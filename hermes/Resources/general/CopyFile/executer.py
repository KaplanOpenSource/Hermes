import os
import shutil

from ...executers.abstractExecuter import abstractExecuter


class CopyFile(abstractExecuter):
    """
    Copies a single file from one location to another.

    Usage:
        Provide the 'Source' path (the file you want to copy) and the 'Target' path (where you want the copy to be placed).

    Example:
        Copying a configuration template file from a project folder to the current simulation directory for customization.
    """


    def _defaultParameters(self):
        return dict(
            output=["Source", "Target"],
            inputs=["Source", "Target"],
            webGUI=dict(JSONSchema="webGUI/copyFile_JSONchema.json",
                        UISchema="webGUI/copyFile_UISchema.json"),
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
            shutil.copy(inputs['Source'], inputs['Target']) # this will change to a flag like the other version.
        else:
            print("=============== empty ===============")

        absSource = os.path.abspath(inputs["Source"])
        absTarget = os.path.abspath(inputs["Target"])

        return dict(Source =absSource,Target=absTarget)
