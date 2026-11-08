from ..abstractConstantExecuter import abstractConstantExecuter


class TurbulenceProperties(abstractConstantExecuter):
    """
    Configures the 'turbulenceProperties' file in OpenFOAM, defining the turbulence model used for the simulation and its corresponding settings.

    Usage:
        Select a turbulence model (e.g., k-epsilon or LES) and specify any necessary coefficients or limits.

    Example:
        Choosing the k-omega SST model to better capture boundary layer separation in an aerodynamic study.
    """


    def __init__(self,JSON):
        super().__init__(JSON,"TurbulenceProperties")

    # def run(self, **inputs):
    #     templateName = "openFOAM/constant/TurbulenceProperties/jinjaTemplate"
    #     template = self._getTemplate(templateName)
    #     effectiveInputs = inputs.get('values',inputs)
    #     output = template.render(**effectiveInputs)
    #     return dict(openFOAMfile=output)