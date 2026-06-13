from scripts.validate_agent_hub_compatibility import validate_manifest


def test_agent_hub_manifest_valid():
    manifest = validate_manifest()
    assert manifest["uniads"]["recommended_endpoint"] == "/v2/sponsor-context"
    assert manifest["uniads"]["preserve_primary_answer"] is True
