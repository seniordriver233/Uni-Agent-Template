from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "uniads.agent.json"
REQUIRED = {
    "name": str,
    "description": str,
    "main_functions": list,
    "ad_compatibility": str,
    "supported_protocols": list,
    "repository_url": str,
}


def validate_manifest(path: Path = MANIFEST) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for key, expected in REQUIRED.items():
        if key not in data:
            errors.append(f"missing {key}")
        elif not isinstance(data[key], expected):
            errors.append(f"{key} must be {expected.__name__}")
    if len(str(data.get("description", "")).strip()) < 20:
        errors.append("description should explain the agent in at least 20 characters")
    if not data.get("main_functions"):
        errors.append("main_functions must include at least one item")
    protocols = {str(item).upper() for item in data.get("supported_protocols", [])}
    if not protocols.intersection({"REST", "SDK", "MCP"}):
        errors.append("supported_protocols should include REST, SDK, or MCP")
    uniads = data.get("uniads", {})
    if not isinstance(uniads, dict):
        errors.append("uniads must be an object")
    else:
        if uniads.get("recommended_endpoint") != "/v2/sponsor-context":
            errors.append("uniads.recommended_endpoint should be /v2/sponsor-context")
        for key in ["preserve_primary_answer", "proxy_only_sponsor_calls", "fail_open", "permission_breakpoint"]:
            if uniads.get(key) is not True:
                errors.append(f"uniads.{key} should be true")
    if errors:
        raise SystemExit("Agent Hub compatibility failed:\n- " + "\n- ".join(errors))
    return data


if __name__ == "__main__":
    manifest = validate_manifest()
    print("Agent Hub compatibility manifest OK")
    print(f"Name: {manifest['name']}")
    print(f"Protocols: {', '.join(manifest['supported_protocols'])}")
