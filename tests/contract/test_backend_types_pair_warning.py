"""The one silent channel between this integration and openccu-loom-client.

`_pair` builds the `isinstance` tuple each platform dispatches on: the
aiohomematic class plus its loom twin. When `openccu-loom-client` is installed
but no longer exposes a twin — renamed, removed, or a version mismatch — the
tuple degrades to the aiohomematic class alone. Every loom entity of that type
then falls out of its platform: a blind loses its tilt, a garage loses its
class, a sound player loses its soundfiles.

That degradation is deliberate, because a hard failure would take the whole
integration down over one missing twin. What it must not be is quiet, and it
used to be: no error, no log, no test. The warning closed the first half.
This closes the second — the warning is the only signal that exists, so
nothing may remove it without a test going red.

The twin-drift test in `test_backend_surface_contract.py` covers the other
case, where both packages are current and a name has moved. It cannot cover
this one: it compares two installed packages, and the failure here is an
installed package that is the wrong version.
"""

from __future__ import annotations

import logging
from types import SimpleNamespace

import pytest

from custom_components.homematicip_local.backend_types import _pair


class _AioClass:
    """Stand-in for an aiohomematic dispatch class."""


class _LoomTwin:
    """Stand-in for its openccu-loom-client twin."""


def test_both_present_yields_the_pair(caplog: pytest.LogCaptureFixture) -> None:
    """The normal case: platforms dispatch on both classes and nothing is logged."""
    module = SimpleNamespace(CustomDpCover=_LoomTwin)
    with caplog.at_level(logging.WARNING):
        assert _pair(_AioClass, "CustomDpCover", module) == (_AioClass, _LoomTwin)
    assert caplog.records == []


def test_a_missing_twin_warns_and_names_it(caplog: pytest.LogCaptureFixture) -> None:
    """The degradation is announced, and the message identifies which twin went."""
    module = SimpleNamespace()  # imported, so the client is installed — but no twin
    with caplog.at_level(logging.WARNING):
        result = _pair(_AioClass, "CustomDpCover", module)

    assert result == (_AioClass,), "the tuple must still degrade rather than fail the setup"
    assert len(caplog.records) == 1, "the only signal this failure has is the warning"
    message = caplog.records[0].getMessage()
    assert "CustomDpCover" in message, "a warning that does not name the twin cannot be acted on"
    assert "version mismatch" in message


def test_no_client_installed_is_silent(caplog: pytest.LogCaptureFixture) -> None:
    """A CCU-only install has no twins to miss, so it must not be warned at."""
    with caplog.at_level(logging.WARNING):
        assert _pair(_AioClass, "CustomDpCover", None) == (_AioClass,)
    assert caplog.records == []
