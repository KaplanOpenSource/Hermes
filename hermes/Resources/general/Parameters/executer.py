from ...executers.abstractExecuter import abstractExecuter


class Parameters(abstractExecuter):
    """
    Defines and passes through a set of parameters to be used by other nodes.

    Usage:
        Use this node to group together several values or configurations that will be needed later in the workflow,
        especially when these values are intended to be used as inputs for a template transformation.

    Example:
        Defining a set of physical constants (viscosity, density) at the start of a project and passing them
        to multiple different OpenFOAM dictionary nodes.
    """


    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=[],
            webGUI=dict(JSONSchema=None,
                        UISchema  =None),
            parameters={}
        )

    def run(self, **inputs):
        ret = dict(transformTemplate="parameterExecuter")
        ret.update(inputs)
        return ret
