"""Provider-neutral tool contracts for an agent or MCP server integration."""
from collections.abc import Callable
from typing import Any
from .analyzer import profile
from .validator import validate


TOOLS: dict[str, Callable[..., Any]] = {"profile_dataset": profile, "validate_dataset": validate}


def tool_schemas() -> list[dict[str, Any]]:
    """Expose JSON-schema tool descriptions for Responses API function calling."""
    return [
        {"type": "function", "name": "profile_dataset", "description": "Profile an in-memory dataset supplied by the host.", "parameters": {"type": "object", "properties": {}, "additionalProperties": False}},
        {"type": "function", "name": "validate_dataset", "description": "Validate an in-memory dataset supplied by the host.", "parameters": {"type": "object", "properties": {}, "additionalProperties": False}},
    ]
