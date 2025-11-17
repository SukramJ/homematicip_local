"""Test the AioHomematic entity helper."""

from __future__ import annotations

from custom_components.homematicip_local.entity_helpers import (
    _ENTITY_DESCRIPTION_BY_DEVICE_AND_PARAM,
    _ENTITY_DESCRIPTION_BY_PARAM,
)


class TestEntityHelper:
    """Tests for entity helper functions."""

    def test_entity_helper(self) -> None:
        """Test entity_helper."""
        params: dict[str, dict[str, dict[str, str]]] = {}
        for platform, eds in _ENTITY_DESCRIPTION_BY_PARAM.items():
            if platform not in params:
                params[str(platform)] = {}
            for edt in eds:
                if isinstance(edt, str):
                    self._add_parameter(edt, params, platform)
                if isinstance(edt, tuple):
                    for ed in edt:
                        self._add_parameter(ed, params, platform)
        for platform, eds in _ENTITY_DESCRIPTION_BY_DEVICE_AND_PARAM.items():
            if platform not in params:
                params[str(platform)] = {}
            for _, edt in eds:
                if isinstance(edt, str):
                    self._add_parameter(edt, params, platform)
                if isinstance(edt, tuple):
                    for ed in edt:
                        self._add_parameter(ed, params, platform)

        assert len(params) == 6

    def _add_parameter(self, ed, params, platform):
        """Add parameter."""
        param = ed.lower()
        if param not in params[str(platform)]:
            params[str(platform)][param] = {}
            params[str(platform)][param]["name"] = param.replace("_", " ").title()
