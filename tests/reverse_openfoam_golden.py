"""OpenFOAM dictionaries reversed into Hermes nodes, frozen against the PyFoam parser.

``hermes/workflow/reverseOpenFOAM.py`` moved from PyFoam to foamlib.  The
inputs under ``data/reverse_openfoam`` are dictionaries copied from the
OpenFOAM 10 tutorials (cavity, pitzDaily, motorBike).
``data/reverse_openfoam_pyfoam`` holds what the PyFoam version of
DictionaryReverser built for each one: the node as JSON, or the exception
it raised (``<file>.error``).  test_reverse_openfoam.py compares the
current code with them.

The goldens can only be regenerated with the PyFoam version of
reverseOpenFOAM.py (commit ed4cd2c) and PyFoam 2023.7 on the path::

    PYTHONPATH=.:<dir with PyFoam> python tests/reverse_openfoam_golden.py
"""
import json
import pathlib
import shutil

DATA = pathlib.Path(__file__).parent / "data"
INPUTS = DATA / "reverse_openfoam"
GOLDEN = DATA / "reverse_openfoam_pyfoam"


def inputFiles():
    return sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob("*") if p.is_file())


def reverse(relativePath):
    """The node DictionaryReverser builds for one dictionary, as plain JSON data."""
    from hermes.workflow.reverseOpenFOAM import DictionaryReverser

    reverser = DictionaryReverser(str(INPUTS / relativePath))
    return json.loads(reverser.to_json_str(reverser.build_node()))


def main():
    import PyFoam  # noqa: F401 -- refuse to freeze the foamlib output as "PyFoam"

    shutil.rmtree(GOLDEN, ignore_errors=True)
    for rel in inputFiles():
        out = GOLDEN / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            node = reverse(rel)
        except Exception as e:  # the old behaviour is part of the record
            out.with_name(out.name + ".error").write_text(f"{type(e).__name__}\n")
        else:
            out.with_name(out.name + ".json").write_text(json.dumps(node, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
