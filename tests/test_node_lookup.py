import pytest
from hermes.utils.node_lookup import get_all_node_types

def test_get_all_node_types():
    # This depends on the environment, but we know where Resources is in this repo
    resources_path = "/raid/users/liora/Development/Hermes/hermes/Resources"
    nodes = get_all_node_types(resources_path)

    assert isinstance(nodes, dict)
    assert len(nodes) > 0

def test_copy_directory_parameters():
    resources_path = "/raid/users/liora/Development/Hermes/hermes/Resources"
    nodes = get_all_node_types(resources_path)

    assert "general.CopyDirectory" in nodes
    params = [p.name for p in nodes["general.CopyDirectory"].parameters]
    # Should find both case versions if we use my current implementation
    assert "Source" in params or "source" in params
    assert "Target" in params or "target" in params

def test_fvschemes_optionality():
    resources_path = "/raid/users/liora/Development/Hermes/hermes/Resources"
    nodes = get_all_node_types(resources_path)

    assert "openFOAM.system.FvSchemes" in nodes
    params = {p.name: p for p in nodes["openFOAM.system.FvSchemes"].parameters}

    # Required parameters (no guards)
    required_vars = [
        "default.ddtScheme",
        "fields",
        "default.interpolationSchemes",
        "default.snGradSchemes",
        "default.wallDist"
    ]
    for var in required_vars:
        assert var in params, f"Parameter {var} should be discovered"
        assert params[var].is_required is True, f"{var} should be required"

    # Optional parameters (guarded by {% if '...' in default -%} or similar)
    optional_vars = [
        "default.gradSchemes.type",
        "default.gradSchemes.name",
        "default.divSchemes.type",
        "default.divSchemes.name",
        "default.divSchemes.parameters",
        "default.laplacianSchemes.type",
        "default.laplacianSchemes.name",
        "default.laplacianSchemes.parameters",
    ]
    for var in optional_vars:
        assert var in params, f"Parameter {var} should be discovered"
        assert params[var].is_required is False, f"{var} should be optional"
