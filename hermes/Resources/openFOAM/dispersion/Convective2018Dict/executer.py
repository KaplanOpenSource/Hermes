from ..abstractDispersionExecuter import abstractDispersionExecuter


class Convective2018Dict(abstractDispersionExecuter):
    """
    Configures the dispersion parameters for convective atmospheric conditions based on a 2018 model specification.

    Usage:
        Provide coefficients and settings that describe how pollutants disperse when thermal turbulence (convection) is dominant in the atmosphere.

    Example:
        Setting up a simulation for a hot summer afternoon where strong solar heating creates unstable air, leading to rapid vertical mixing of pollutant plumes.
    """

    def __init__(self,JSON):
        super().__init__(JSON,"IndoorDict")
