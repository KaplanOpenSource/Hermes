from ..abstractConstantExecuter import abstractConstantExecuter


class momentumTransport(abstractConstantExecuter):
    """
    Configures the 'momentumTransport' file in OpenFOAM, which specifies how momentum is transported through the fluid (typically by selecting and configuring a turbulence model).

    Usage:
        Choose a transport model (e.g., RAS or LES) and define its specific parameters.

    Example:
        Setting up a Reynolds-Averaged Navier-Stokes (RANS) simulation to efficiently compute time-averaged flow patterns around an obstacle.
    """


    def __init__(self,JSON):
        super().__init__(JSON,"momentumTransport")

    # def run(self, **inputs):
    #     templateName = "openFOAM/constant/TurbulenceProperties/jinjaTemplate"
    #     template = self._getTemplate(templateName)
    #     effectiveInputs = inputs.get('values',inputs)
    #     output = template.render(**effectiveInputs)
    #     return dict(openFOAMfile=output)