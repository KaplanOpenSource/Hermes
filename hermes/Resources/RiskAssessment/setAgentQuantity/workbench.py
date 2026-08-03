
# import FreeCAD modules
# import FreeCAD, FreeCADGui, WebGui

# Hermes modules
# from hermes.Resources.workbench.HermesNode import WebGuiNode
from ...workbench.HermesNode import WebGuiNode


# =============================================================================
# RunPythonCode
# =============================================================================
class RunPythonCode(WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def guiToExecute(self, obj):
        ''' convert the json data to "input_parameters" structure '''

        parameters = dict()
        parameters["ProjectName"] = obj.ProjectName
        parameters["LSMPath"] = obj.LSMPath
        parameters["policy"] = obj.policy
        if "formData" in self.nodeData["WebGui"]:
            parameters["Parameters"] = self.nodeData["WebGui"]["formData"]


        return parameters

    def executeToGui(self, obj, parameters):
        ''' import the "input_parameters" data into the json obj data '''

        obj.ProjectName = parameters["ProjectName"]
        obj.LSMPath = parameters["LSMPath"]
        obj.policy = parameters["policy"]
        obj.Parameters = parameters["Parameters"]

        if len(parameters["Parameters"]) > 0:
            self.nodeData["WebGui"]["formData"] = parameters["Parameters"]
