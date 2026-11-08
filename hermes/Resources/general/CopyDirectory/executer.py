import os
import shutil

from ...executers.abstractExecuter import abstractExecuter


class CopyDirectory(abstractExecuter):
    """
    Copies an entire folder (and all its contents) from one location to another.

    Usage:
        Provide the 'Source' path of the folder you wish to copy and the 'Target' path where the copies should be placed.

    Example:
        Backing up a set of simulation input files into a separate archival directory before starting a new run.
    """


    def _defaultParameters(self):
        return dict(
            output=["Source,Target"],
            inputs=["Source","Target"],
            webGUI=dict(JSONSchema="webGUI/copyDirectory_JSONchema.json",
                        UISchema  = "webGUI/copyDirectory_UISchema.json"),
            parameters={}
        )
    
    @staticmethod
    def testParamValues(params: dict[str, any]):
        for param in ["Source", "Target"]:
            passed, status_message = abstractExecuter.checkParamType(params, param, str, required=True)
            if not passed:
                return passed, status_message

        return True, ""

    def run(self, **inputs):
        if (len(inputs["Source"]) > 0 and len(inputs["Target"]) > 0):
            shutil.copytree(inputs['Source'],inputs['Target'],dirs_exist_ok=inputs.get("dirs_exist_ok",True))
        else:
            print("=============== empty ===============")

        absSource = os.path.abspath(inputs["Source"])
        absTarget = os.path.abspath(inputs["Target"])

        return dict(Source =absSource,Target=absTarget)