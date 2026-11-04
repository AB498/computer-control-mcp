"""
Tests for execute_actions tool in Computer Control MCP.
"""

import pytest
import json
import pyautogui
from computer_control_mcp.core import mcp

@pytest.mark.asyncio
async def test_execute_actions_wait_and_typing():
    actions = [
        {"type": "wait", "milliseconds": 20},
        {"type": "press", "keys": "shift"},
    ]
    res = await mcp.call_tool("execute_actions", {
        "actions": actions,
        "failsafe": False
    })
    
    content_list = res[0] if isinstance(res, tuple) else res
    text_content = content_list[0].text
    result = json.loads(text_content)
    
    assert result["success"] is True
    assert result["executed_count"] == 2
    assert result["total_actions"] == 2
    assert len(result["results"]) == 2
    assert result["results"][0]["action"] == "wait"
    assert result["results"][1]["action"] == "press"


@pytest.mark.asyncio
async def test_execute_actions_curve_and_move():
    actions = [
        {"type": "move", "x": 500, "y": 500},
        {"type": "curve", "points": [[510, 510], [520, 520], [530, 530]], "interval_ms": 2},
    ]
    res = await mcp.call_tool("execute_actions", {
        "actions": actions,
        "failsafe": False
    })
    
    content_list = res[0] if isinstance(res, tuple) else res
    text_content = content_list[0].text
    result = json.loads(text_content)
    
    assert result["success"] is True
    assert result["executed_count"] == 2
    assert "Followed curve with 3 points" in result["results"][1]["details"]


@pytest.mark.asyncio
async def test_execute_actions_fail_fast():
    actions = [
        {"type": "wait", "milliseconds": 10},
        {"type": "non_existent_action_type"},
        {"type": "wait", "milliseconds": 10},
    ]
    res = await mcp.call_tool("execute_actions", {
        "actions": actions,
        "fail_fast": True
    })
    
    content_list = res[0] if isinstance(res, tuple) else res
    text_content = content_list[0].text
    result = json.loads(text_content)
    
    assert result["success"] is False
    assert result["executed_count"] == 1
    assert result["results"][1]["success"] is False
    # Third action should not have run because fail_fast is True
    assert len(result["results"]) == 2
