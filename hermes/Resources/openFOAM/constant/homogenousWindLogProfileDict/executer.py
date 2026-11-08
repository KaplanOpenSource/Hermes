from ..abstractConstantExecuter import abstractConstantExecuter


class homogenousWindLogProfileDict(abstractConstantExecuter):
    """
    Configures the 'homogenousWindLogProfileDict' file in OpenFOAM, used to define a uniform wind profile across the simulation domain.

    Usage:
        Specify parameters for the wind profile, such as reference velocity and height.

    Example:
        Setting up a simplified neutral atmospheric boundary layer with a constant wind speed at a specific reference height.
    """

    def __init__(self,JSON):
        super().__init__(JSON,"homogenousWindLogProfileDict")
