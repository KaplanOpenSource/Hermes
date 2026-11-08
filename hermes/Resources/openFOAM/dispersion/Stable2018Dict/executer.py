from ..abstractDispersionExecuter import abstractDispersionExecuter


class Stable2018Dict(abstractDispersionExecuter):
    """
    Configures the dispersion parameters for stable atmospheric conditions based on a 2018 model specification.

    Usage:
        Provide coefficients and settings that describe how pollutants disperse in a stable atmosphere, which typically inhibits vertical mixing.

    Example:
        Simulating a clear night with a temperature inversion, where pollutants remain trapped near the ground and travel further downwind than they would in unstable conditions.
    """

    def __init__(self,JSON):
        super().__init__(JSON,"IndoorDict")
