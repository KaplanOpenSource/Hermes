from ....executers.abstractExecuter import abstractExecuter


class GeometryDefinerExecuter(abstractExecuter):
    """
    Defines the geometric boundaries and surfaces of the simulation domain, typically creating files used for mesh refinement.

    Usage:
        Provide descriptions of the objects (e.g., STL files or primitives) that define the physical obstacles and boundaries in your scene.

    Example:
        Importing a 3D model of a building to be used as a boundary that the wind must flow around in an urban dispersion study.
    """


    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=[],
            webGUI=dict(JSONSchema=None,
                        UISchema=None),
            parameters={}
        )

    def run(self, **inputs):
        return dict()