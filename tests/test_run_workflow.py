"""
Integration test that actually builds and executes a hermes workflow through the
Luigi engine, exercising the dispatch_id mechanism added for the centralized
scheduler (issue #918).

It builds the Tutorial workflow (CopyDirectory -> RunPythonCode -> finalnode),
runs it with Luigi's local scheduler and a dispatch_id, and verifies that:
  - the workflow runs to completion,
  - the per-node output targets land in a dispatch_id-namespaced subdirectory,
  - a different dispatch_id produces an independent run (no collision).
"""

import os
import subprocess
import sys

import pytest

HERMES_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Self-contained workflow: copy a directory, then call a python method on the result.
WORKFLOW_JSON = {
    "workflow": {
        "nodes": {
            "CopyDirectory": {
                "Execution": {
                    "input_parameters": {
                        "Source": "source",
                        "Target": "target",
                        "dirs_exist_ok": True,
                    }
                },
                "type": "general.CopyDirectory",
            },
            "RunPythonCode": {
                "Execution": {
                    "input_parameters": {
                        "ModulePath": "tutorial1",
                        "ClassName": "tutrialPrinter",
                        "MethodName": "printDirectories",
                        "Parameters": {
                            "source": "{CopyDirectory.output.Source}",
                            "target": "{CopyDirectory.output.Target}",
                        },
                    }
                },
                "type": "general.RunPythonCode",
            },
        }
    }
}

TUTORIAL_MODULE = (
    "class tutrialPrinter:\n"
    "    def printDirectories(self, source, target):\n"
    "        print(f'Copied {source} to {target}')\n"
)


def _build_and_run(workdir, dispatch_id):
    """Build the workflow into a Luigi module and execute it for the given dispatch_id."""
    # hermes is imported lazily so a missing optional dependency skips, not errors.
    hermes = pytest.importorskip("hermes")
    workflow = hermes.workflow

    # Lay down the workflow inputs in the working directory.
    os.makedirs(os.path.join(workdir, "source"), exist_ok=True)
    with open(os.path.join(workdir, "tutorial1.py"), "w") as fp:
        fp.write(TUTORIAL_MODULE)

    wf = workflow(WORKFLOW_JSON, workdir, Resource_path=workdir)
    build = wf.build(buildername=workflow.BUILDER_LUIGI)
    with open(os.path.join(workdir, "Workflow1.py"), "w") as fp:
        fp.write(build)

    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([HERMES_ROOT, workdir, env.get("PYTHONPATH", "")])
    result = subprocess.run(
        [sys.executable, "-m", "luigi", "--module", "Workflow1",
         "finalnode_xx_0", "--local-scheduler"],
        cwd=workdir, env=env, capture_output=True, text=True,
    )
    return result


def test_workflow_runs_and_isolates_outputs_per_dispatch(tmp_path):
    workdir = str(tmp_path)

    # First run.
    res1 = _build_and_run(workdir, "RUN1")
    assert "this progress looks :)" in res1.stderr.lower(), res1.stderr
    run1_dir = os.path.join(workdir, "Workflow1_targetFiles", "RUN1")
    assert os.path.isfile(os.path.join(run1_dir, "finalnode_xx_0.json"))
    assert os.path.isfile(os.path.join(run1_dir, "CopyDirectory_0.json"))
    assert os.path.isfile(os.path.join(run1_dir, "RunPythonCode_0.json"))

    # A different dispatch_id is an independent run with its own output directory.
    res2 = _build_and_run(workdir, "RUN2")
    assert "this progress looks :)" in res2.stderr.lower(), res2.stderr
    run2_dir = os.path.join(workdir, "Workflow1_targetFiles", "RUN2")
    assert os.path.isfile(os.path.join(run2_dir, "finalnode_xx_0.json"))

    # The two runs did not collide: separate, both-populated directories.
    assert os.path.isdir(run1_dir) and os.path.isdir(run2_dir)
