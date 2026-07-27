"""The parity ratchet: device models whose entity-set parity is ENFORCED.

The three-way parity suite always *reports* every difference between the
planes, but only entities backed by a model listed here (plus all hub/central
entities, which carry no device model) *fail* ``test_entity_set_parity`` in a
widened run (``GODEVCCU_E2E_DEVICES`` set). In the default 4-device run the
whole set is enforced regardless of this list.

Ratchet workflow — widen only, never loosen:

1. Run the comprehensive report::

       GODEVCCU_E2E_DEVICES=all venv/bin/pytest tests/e2e -m e2e -n0 -s

2. Read the ``PARITY REPORT``: its ``promotable_models`` list names every
   model that is already clean across all three planes but not yet enforced.
3. Add those models to ``ENFORCED_MODELS`` and commit — from then on they can
   never silently regress.
4. A model may only ever be REMOVED together with a changelog entry that
   explains the accepted regression.

The end state of the ratchet is every godevccu model enforced, at which point
``GODEVCCU_E2E_DEVICES=all`` is a green gate and this list equals the full
device set.
"""

from __future__ import annotations

from typing import Final

# godevccu-e2e's fixed default set (one device per HA domain shape): cover,
# switch/meter, wall thermostat, smoke detector/siren. These are the seed —
# they are exactly the models the default run has always enforced.
ENFORCED_MODELS: Final[frozenset[str]] = frozenset(
    {
        "HmIP-BROLL",
        "HmIP-BSM",
        "HmIP-BWTH",
        "HmIP-SWSD",
    }
)
