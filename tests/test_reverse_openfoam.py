"""DictionaryReverser on real OpenFOAM 10 dictionaries, compared with the PyFoam version.

See reverse_openfoam_golden.py for where the inputs and goldens come from.
Values are compared by meaning: an OpenFOAM value kept as text
("uniform (1 0 0)", "[0 1 -1 0 0 0 0]") matches when both texts parse to the
same value, so "uniform 0" and "uniform 0.0" are equal.
"""
import json
import pathlib
import sys

import numpy
import pytest
from foamlib import FoamFile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from reverse_openfoam_golden import GOLDEN, inputFiles, reverse  # noqa: E402

# Entries the PyFoam version got wrong; removed from both sides before comparing
# and checked by test_entries_pyfoam_got_wrong_are_right_now.
WRONG_IN_PYFOAM = {
    ("motorBike/system/snappyHexMeshDict", ("meshQualityControls",)):
        "the #include became an entry named '0'",
    ("pitzDaily/system/fvSolution", ("relaxationFactors", "equations")):
        "equations { U 0.9; \".*\" 0.9; } collapsed to the number 0.9",
}

# Dictionaries PyFoam could not parse at all, now reversed: name -> what to check.
FIXED = {
    "pitzDaily/system/controlDict": "PyFoamParserError on the #includeFunc lines in functions",
}


def _openfoamValue(text):
    return FoamFile.loads(f"v {text};".encode())["v"]


def _assertSame(new, old, where):
    if isinstance(old, dict):
        assert isinstance(new, dict), f"{where}: {new!r}"
        # PyFoam's DictProxy keeps regex keys out of items(), so the PyFoam version lost
        # every '"(a|b).*"' entry; checked on its own below.
        new = {k: v for k, v in new.items() if k in old or not k.startswith('"')}
        assert sorted(new) == sorted(old), f"{where}: keys {sorted(new)} != {sorted(old)}"
        for key in old:
            _assertSame(new[key], old[key], f"{where}/{key}")
    elif isinstance(old, list):
        assert isinstance(new, list) and len(new) == len(old), f"{where}: {new!r} != {old!r}"
        for i, (n, o) in enumerate(zip(new, old)):
            _assertSame(n, o, f"{where}[{i}]")
    elif isinstance(old, str) and isinstance(new, str) and new != old:
        _assertSame(_plain(_openfoamValue(new)), _plain(_openfoamValue(old)), f"{where} ({new!r} vs {old!r})")
    elif isinstance(old, (int, float)) and not isinstance(old, bool):
        assert numpy.isclose(new, old), f"{where}: {new!r} != {old!r}"
    else:
        assert new == old, f"{where}: {new!r} != {old!r}"


def _plain(value):
    """foamlib values as lists/numbers, for comparing two parsed texts."""
    if isinstance(value, numpy.ndarray):
        return value.tolist()
    if isinstance(value, tuple):
        return [_plain(v) for v in value]
    if hasattr(value, "_asdict"):  # DimensionSet
        return list(value)
    return value


def _inputs(node):
    (name, body), = node.items()
    return body["Execution"]["input_parameters"]


def _drop(tree, path):
    for key in path[:-1]:
        tree = tree[key]
    tree.pop(path[-1])


@pytest.mark.parametrize("rel", [r for r in inputFiles() if not (GOLDEN / (r + ".error")).exists()])
def test_the_node_matches_the_pyfoam_one(rel):
    new, expected = reverse(rel), json.loads((GOLDEN / (rel + ".json")).read_text())
    for (wrongRel, path) in WRONG_IN_PYFOAM:
        if wrongRel == rel:
            _drop(_inputs(new), path)
            _drop(_inputs(expected), path)
    _assertSame(new, expected, rel)


def test_entries_pyfoam_got_wrong_are_right_now():
    snappy = _inputs(reverse("motorBike/system/snappyHexMeshDict"))
    assert snappy["meshQualityControls"] == {"#include": '"meshQualityDict"'}
    fvSolution = _inputs(reverse("pitzDaily/system/fvSolution"))
    assert fvSolution["relaxationFactors"]["equations"] == {"U": 0.9, '".*"': 0.9}


def test_every_dictionary_pyfoam_failed_on_is_listed():
    failed = {r for r in inputFiles() if (GOLDEN / (r + ".error")).exists()}
    assert failed == set(FIXED)


def test_a_control_dict_with_include_func_is_reversed():
    values = reverse("pitzDaily/system/controlDict")["controlDict"]["Execution"]["input_parameters"]["values"]
    assert values["application"] == "simpleFoam"
    assert values["endTime"] == 2000
    assert "functions" in values


def test_regex_keys_are_kept():
    """The PyFoam version dropped them: the layer settings of the motorBike surfaces
    and the residual control of the turbulence fields were missing from the node."""
    snappy = reverse("motorBike/system/snappyHexMeshDict")["snappyHexMeshDict"]["Execution"]["input_parameters"]
    assert snappy["addLayersControls"]["layers"]['"(lowerWall|motorBike).*"'] == {"nSurfaceLayers": 1}
    simple = reverse("pitzDaily/system/fvSolution")["fvSolution"]["Execution"]["input_parameters"]["SIMPLE"]
    assert '"(k|epsilon|omega|f|v2)"' in simple["residualControl"]


def test_field_values_stay_openfoam_text_for_the_templates():
    """The workflow templates write these strings back into the case as they are."""
    node = reverse("cavity/0/U")["U"]["Execution"]["input_parameters"]
    assert numpy.allclose(_openfoamValue(node["internalField"]), [0, 0, 0])
    assert node["internalField"].startswith("uniform")
    assert node["boundaryField"]["movingWall"]["value"].startswith("uniform")
    assert isinstance(node["dimensions"], str)


def test_reversing_does_not_need_pyfoam():
    reverse("cavity/system/controlDict")
    assert not any(name == "PyFoam" or name.startswith("PyFoam.") for name in sys.modules)
