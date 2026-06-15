import os

from ...executers.abstractExecuter import abstractExecuter
import pydoc
import sys

class RunPythonMethod(abstractExecuter):
    """
        Executes the function in the class.

        inputs:
            classpath : str, The class path string to the class
            funcName  : str, The name of the function to run .
            parameters : dict, The parameters for the function.
    """

    def _defaultParameters(self):
        return dict(
            output=["status"],

            inputs=["Class", "method"],
            webGUI=dict(JSONSchema="webGUI/pythonExecuter_JSONchema.json",
                        UISchema="webGUI/pythonExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        # newobj = pydoc.locate(inputs['classpath'])()
        # func   = getattr(newobj,input["funcName"])
        # ret = func(**inputs['parameters'])
        self.logger.info("Starting run of run python class method")

        obj = inputs["ClassName"]
        #full_json = inputs["Parameters"].get("fullJSON", {})  # default to empty
        #newobj = objcls(full_json)

        func   = getattr(obj,inputs["MethodName"])
        ret = func(**inputs['Parameters'])
        return dict(pythonMethodExecuter="pythonMethodExecuter",Return=ret)