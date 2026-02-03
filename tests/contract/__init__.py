"""
Contract tests for homematicip_local stability guarantees.

STABILITY GUARANTEE
-------------------
These tests define the stable API contract for homematicip_local integration.
Any change that breaks these tests requires a MAJOR version bump.

The contract ensures that:
1. Services are properly registered and accessible
2. Entity methods have stable signatures
3. Service schemas are consistent

See aiohomematic contract tests for reference.
"""

from __future__ import annotations
