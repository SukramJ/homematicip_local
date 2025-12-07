"""Entity description registry for Homematic(IP) Local."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
import logging
from typing import TYPE_CHECKING, Final

from aiohomematic.const import DataPointCategory

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.helpers.entity import EntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True, slots=True)
class EntityDescriptionRule:
    """
    A rule that maps data point characteristics to an entity description.

    Rules are matched in priority order. The first matching rule wins.
    All specified criteria must match (AND logic).

    Attributes:
        description: The entity description to use when this rule matches
        category: Required - the data point category this rule applies to
        parameters: Optional tuple of parameter names to match
        devices: Optional tuple of device model prefixes to match
        unit: Optional unit string to match
        postfix: Optional data point name postfix to match
        var_name_contains: Optional substring that must appear in variable name
        priority: Higher priority rules are checked first (default: 0)
        matcher: Optional custom matching function for complex cases

    Example:
        # Simple parameter match
        EntityDescriptionRule(
            category=DataPointCategory.SENSOR,
            parameters=("TEMPERATURE", "ACTUAL_TEMPERATURE"),
            description=temperature_sensor_description,
        )

        # Device-specific override with higher priority
        EntityDescriptionRule(
            category=DataPointCategory.SENSOR,
            parameters=("ACTUAL_TEMPERATURE",),
            devices=("HmIP-BS", "HmIP-PS"),
            priority=10,
            description=diagnostic_temperature_description,
        )

    """

    description: EntityDescription
    category: DataPointCategory

    # Matching criteria (all specified must match)
    parameters: tuple[str, ...] | None = None
    devices: tuple[str, ...] | None = None
    unit: str | None = None
    postfix: str | None = None
    var_name_contains: str | None = None

    # Rule metadata
    priority: int = 0

    # Custom matcher for complex cases (excluded from comparison)
    matcher: Callable[[object], bool] | None = field(default=None, compare=False)

    def matches(
        self,
        *,
        category: DataPointCategory,
        parameter: str | None = None,
        device_model: str | None = None,
        unit: str | None = None,
        postfix: str | None = None,
        var_name: str | None = None,
    ) -> bool:
        """
        Check if this rule matches the given data point characteristics.

        All specified criteria must match. Criteria that are None are skipped.
        """
        # Category must always match
        if self.category != category:
            return False

        # Check parameter match
        if self.parameters is not None:
            if parameter is None:
                return False
            param_upper = parameter.upper()
            if not any(p.upper() == param_upper for p in self.parameters):
                return False

        # Check device model match (prefix matching)
        if self.devices is not None:
            if device_model is None:
                return False
            if not any(device_model.startswith(d) for d in self.devices):
                return False

        # Check unit match
        if self.unit is not None and unit != self.unit:
            return False

        # Check postfix match
        if self.postfix is not None:
            if postfix is None:
                return False
            if postfix.upper() != self.postfix.upper():
                return False

        # Check variable name contains
        if self.var_name_contains is not None:
            if var_name is None:
                return False
            if self.var_name_contains.lower() not in var_name.lower():
                return False

        return True


class EntityDescriptionRegistry:
    """
    Central registry for entity description rules.

    The registry maintains rules organized by category and provides
    efficient lookup using indexes and caching.

    Usage:
        registry = EntityDescriptionRegistry()

        # Register rules
        registry.register(rule1)
        registry.register(rule2)
        # ... or register many at once
        registry.register_all([rule1, rule2, rule3])

        # Find matching description
        description = registry.find(
            category=DataPointCategory.SENSOR,
            parameter="TEMPERATURE",
            device_model="HmIP-STHD",
        )
    """

    def __init__(self) -> None:
        """Initialize the registry."""
        # Rules organized by category for efficient lookup
        self._rules_by_category: dict[DataPointCategory, list[EntityDescriptionRule]] = defaultdict(list)

        # Default descriptions per category
        self._defaults: dict[DataPointCategory, EntityDescription] = {}

        # Flag to track if rules need re-sorting
        self._needs_sort: bool = False

    def find(
        self,
        *,
        category: DataPointCategory,
        parameter: str | None = None,
        device_model: str | None = None,
        unit: str | None = None,
        postfix: str | None = None,
        var_name: str | None = None,
    ) -> EntityDescription | None:
        """
        Find the best matching entity description.

        Returns the description from the highest-priority matching rule,
        or the default for the category if no rule matches.

        Args:
            category: The data point category
            parameter: The parameter name (e.g., "TEMPERATURE")
            device_model: The device model (e.g., "HmIP-STHD")
            unit: The unit of measurement
            postfix: The data point name postfix
            var_name: The variable name (for hub data points)

        Returns:
            The matching EntityDescription or None

        """
        # Ensure rules are sorted by priority
        self._ensure_sorted()

        # Use cached lookup
        return self._find_cached(
            category=category,
            parameter=parameter,
            device_model=device_model,
            unit=unit,
            postfix=postfix,
            var_name=var_name,
        )

    def get_stats(self) -> dict[str, int]:
        """Get statistics about registered rules."""
        return {cat.name: len(rules) for cat, rules in self._rules_by_category.items()}

    def register(self, rule: EntityDescriptionRule) -> None:
        """
        Register a single rule.

        Rules are automatically sorted by priority on next lookup.
        """
        self._rules_by_category[rule.category].append(rule)
        self._needs_sort = True
        # Invalidate cache
        self._find_cached.cache_clear()

    def register_all(self, rules: list[EntityDescriptionRule]) -> None:
        """Register multiple rules at once."""
        for rule in rules:
            self._rules_by_category[rule.category].append(rule)
        self._needs_sort = True
        self._find_cached.cache_clear()

    def set_default(
        self,
        category: DataPointCategory,
        description: EntityDescription,
    ) -> None:
        """Set the default description for a category."""
        self._defaults[category] = description

    def validate(self) -> list[str]:
        """
        Validate all registered rules.

        Returns a list of warning messages for potential issues.
        """
        warnings: list[str] = []
        seen_keys: set[str] = set()

        for category, rules in self._rules_by_category.items():
            for rule in rules:
                key = rule.description.key
                if key in seen_keys:
                    warnings.append(f"Duplicate description key '{key}' in category {category.name}")
                seen_keys.add(key)

        return warnings

    def _ensure_sorted(self) -> None:
        """Sort rules by priority (descending) if needed."""
        if not self._needs_sort:
            return

        for category in self._rules_by_category:
            self._rules_by_category[category].sort(
                key=lambda r: r.priority,
                reverse=True,
            )

        self._needs_sort = False

    @lru_cache(maxsize=512)
    def _find_cached(
        self,
        *,
        category: DataPointCategory,
        parameter: str | None = None,
        device_model: str | None = None,
        unit: str | None = None,
        postfix: str | None = None,
        var_name: str | None = None,
    ) -> EntityDescription | None:
        """Find matching description using cache."""
        rules = self._rules_by_category.get(category, [])

        for rule in rules:
            if rule.matches(
                category=category,
                parameter=parameter,
                device_model=device_model,
                unit=unit,
                postfix=postfix,
                var_name=var_name,
            ):
                return rule.description

        # Return default if no rule matched
        return self._defaults.get(category)


# Global registry instance
REGISTRY: Final[EntityDescriptionRegistry] = EntityDescriptionRegistry()
