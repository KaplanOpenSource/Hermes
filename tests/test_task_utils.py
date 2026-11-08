"""
Regression tests for the parameter token / path resolution in the Luigi task utils.

Covers the error:
    The token extractCenterline.Execution.input_parameters.ClassName not found in {...}
"""

import pytest

from hermes.engines.luigi.taskUtils import utils


def _make_utils():
    return utils()


def _task_params():
    return {
        "extractCenterline": {
            "Execution": {
                "input_parameters": {
                    "ClassName": "aaabbb",
                    "MethodName": "some_method_name",
                    "ModulePath": "some_path",
                    "Parameters": {
                        "project_name": "project_name",
                        "workflow_name": "workflow_name",
                    },
                }
            },
            "output": {"Return": "some_return_value"},
            "type": "general.RunPythonCode",
        }
    }


def test_parse_and_evaluate_path_resolves_node_execution_input_parameters():
    utils_instance = _make_utils()
    token = "{extractCenterline.Execution.input_parameters.ClassName}"
    assert utils_instance._parseAndEvaluatePath(token, _task_params()) == "aaabbb"


def test_parse_and_evaluate_path_resolves_node_input_parameters():
    utils_instance = _make_utils()
    token = "{extractCenterline.input_parameters.ClassName}"
    assert utils_instance._parseAndEvaluatePath(token, _task_params()) == "aaabbb"