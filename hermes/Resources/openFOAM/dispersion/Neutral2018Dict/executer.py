from ..abstractDispersionExecuter import abstractDispersionExecuter


class Neutral2018Dict(abstractDispersionExecuter):
    """
    Configures the dispersion parameters for neutral atmospheric conditions based on a 2018 model specification.

    Usage:
        Provide coefficients and settings that describe how pollutants disperse in a neutrally stable atmosphere, where thermal effects are minimal.

    Example:
        Setting up a simulation for an overcast day or nighttime when the vertical temperature gradient is near adiabatic, leading to standard Gaussian-like dispersion patterns.
    """

    def __init__(self,JSON):
        super().__init__(JSON,"IndoorDict")
