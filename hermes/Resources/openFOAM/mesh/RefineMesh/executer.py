from ....general import JinjaTransform


class RefineMesh(JinjaTransform):
    """
    Configures the process of locally refining the mesh density in specific regions of interest to improve simulation accuracy.

    Usage:
        Specify the areas (e.g., near a source or an obstacle) where you need a finer grid and the level of refinement required.

    Example:
        Increasing the mesh resolution specifically around a chemical release point to accurately capture high concentration gradients.
    """


    def _defaultParameters(self):
        return dict(
            output=["openFOAMfile"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/BlockMeshExecuter_JSONchema.json",
                        UISchema="webGUI/BlockMeshExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        # get the  name of the template
        templateName = "openFOAM/mesh/RefineMesh/jinjaTemplate"

        template = self._getTemplate(templateName)
        # render jinja for the choosen template
        output = template.render(**inputs)

        return dict(openFOAMfile=output)