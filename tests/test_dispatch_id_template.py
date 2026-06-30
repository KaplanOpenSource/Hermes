"""
Tests for the dispatch_id support added to the generated Luigi node template
(issue #918).

The template (hermes/engines/luigi/pythonClassBase.py) only depends on jinja2 and
pprint, so it is loaded directly here without importing the full hermes package.
This keeps the test runnable without hermes' heavier runtime dependencies.
"""

import ast
import importlib.util
import os

TEMPLATE_MODULE = os.path.join(
    os.path.dirname(__file__), "..", "hermes", "engines", "luigi", "pythonClassBase.py"
)


def _load_transform():
    spec = importlib.util.spec_from_file_location("pythonClassBase", TEMPLATE_MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.transform


class _StubTaskWrapper:
    """Minimal task wrapper exposing every attribute the template renders."""

    def __init__(self, name, required=None):
        self.taskfullname = name
        self.taskJSON = {"Execution": {"input_parameters": {}}}
        self.task_workflowJSON = {"workflow": {"version": 1}}
        self.input_parameters = {}
        self.formData = self.files = self.Schema = None
        self.uiSchema = self.task_Properties = self.task_webGui = None
        self.requiredTasks = required or {}

    def getExecuterPackage(self):
        return "stub_executer"

    def getExecuterClass(self):
        return "StubExecuter"


def test_template_source_declares_propagates_and_isolates():
    template = _load_transform()._basicLuigiTemplate
    # Declared on every generated node class so the central scheduler can tell runs apart.
    assert 'dispatch_id = luigi.Parameter(default="")' in template
    # Propagated to required tasks (Luigi does not thread parameters automatically).
    assert "dispatch_id=self.dispatch_id" in template
    # Used to isolate per-dispatch output targets.
    assert "self.dispatch_id or" in template


def test_rendered_module_is_valid_python_with_dispatch_id():
    transform = _load_transform()
    child = _StubTaskWrapper("Parameters_0")
    final = _StubTaskWrapper("finalnode_xx_0", required={"Parameters": child})

    rendered = transform().transform(final, "/tmp/wd")

    assert 'dispatch_id = luigi.Parameter(default="")' in rendered
    # The required task is instantiated with the parent's dispatch_id.
    assert "Parameters_0(dispatch_id=self.dispatch_id)" in rendered
    # Output target is namespaced by dispatch_id.
    assert "dispatchSubdir = self.dispatch_id or" in rendered
    # And the generated source is valid Python.
    ast.parse(rendered)
