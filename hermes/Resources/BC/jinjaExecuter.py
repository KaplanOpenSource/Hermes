from ..executers.jinjaExecuters import jinjaExecuter


class BC(jinjaExecuter):
    """
    Generates OpenFOAM boundary condition (BC) files using Jinja templates.

    Usage:
        Provide the parameters required by the 'openFOAM/mesh/BC' template to define how variables behave at the boundaries of the simulation domain.

    Example:
        Defining a fixed-value velocity for an inlet patch and a zero-gradient condition for the outlet, ensuring a consistent flow through the domain.
    """


    def run(self, **inputs):

        template = self._getTemplate("openFOAM/mesh/BC")
        output = template.render(**inputs)
        return dict(openFOAMfile=output)