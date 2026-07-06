
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
        parameters["Template"] = obj.Template
        parameters["SimulationParameters"] = obj.SimulationParameters
        parameters["SimulationName"] = obj.SimulationName
        parameters["saveMode"] = obj.saveMode
        parameters["topography"] = obj.topography
        parameters["stations"] = obj.stations
        parameters["canopy"] = obj.canopy
        parameters["depositionRates"] = obj.depositionRates
        if "formData" in self.nodeData["WebGui"]:
            parameters["Parameters"] = self.nodeData["WebGui"]["formData"]


        return parameters

    def executeToGui(self, obj, parameters):
        ''' import the "input_parameters" data into the json obj data '''

        obj.ProjectName = parameters["ProjectName"]
        obj.Template = parameters["Template"]
        obj.SimulationParameters = parameters["SimulationParameters"]
        obj.SimulationName = parameters["SimulationName"]
        obj.saveMode = parameters["saveMode"]
        obj.topography = parameters["topography"]
        obj.stations = parameters["stations"]
        obj.canopy = parameters["canopy"]
        obj.depositionRates = parameters["depositionRates"]

        if len(parameters["Parameters"]) > 0:
            self.nodeData["WebGui"]["formData"] = parameters["Parameters"]
