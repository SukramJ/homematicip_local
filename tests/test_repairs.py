"""
Unit tests for custom_components.homematicip_local.repairs.

These tests aim for 100% coverage of the lightweight repairs flow helper:
- Creating the flow exposes the confirm step with placeholders populated from the issue_id.
- Confirming the flow triggers and awaits a registered callback and deletes the issue.
- Confirming the flow with no callback still closes the issue gracefully.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from custom_components.homematicip_local import repairs as hm_repairs


@pytest.mark.asyncio
async def test_async_create_fix_flow_and_confirm_with_callback(hass) -> None:
    """It should show a confirm form and, upon confirm, run the callback and delete the issue."""
    issue_id = "devices_delayed|intf123|ABC0001"

    # Prepare a callback that we verify was awaited
    cb = AsyncMock()
    hm_repairs.REPAIR_CALLBACKS[issue_id] = cb

    # Create the flow
    flow = await hm_repairs.async_create_fix_flow(hass, issue_id, data={})

    # Initial step should be a form with placeholders from issue id parts
    step_init = await flow.async_step_init()
    assert step_init["type"] == "form"
    placeholders = step_init["description_placeholders"]
    assert placeholders["issue_id"] == issue_id
    assert placeholders["interface_id"] == "intf123"
    assert placeholders["address"] == "ABC0001"

    # Confirm the flow and ensure it deletes the issue and awaits the callback
    with patch("custom_components.homematicip_local.repairs.async_delete_issue") as delete_issue:
        result = await flow.async_step_confirm(user_input={})

    delete_issue.assert_called_once_with(hass=hass, domain=hm_repairs.DOMAIN, issue_id=issue_id)
    cb.assert_awaited()
    assert result["type"] == "create_entry"


@pytest.mark.asyncio
async def test_confirm_without_callback_still_closes_issue(hass) -> None:
    """If no callback is registered, confirming should still close the issue without error."""
    issue_id = "devices_delayed|intfX|ADDRY"

    # No callback registered: ensure dict doesn't contain our key
    hm_repairs.REPAIR_CALLBACKS.pop(issue_id, None)

    flow = await hm_repairs.async_create_fix_flow(hass, issue_id, data={})

    with patch("custom_components.homematicip_local.repairs.async_delete_issue") as delete_issue:
        result = await flow.async_step_confirm(user_input={})

    delete_issue.assert_called_once_with(hass=hass, domain=hm_repairs.DOMAIN, issue_id=issue_id)
    assert result["type"] == "create_entry"
