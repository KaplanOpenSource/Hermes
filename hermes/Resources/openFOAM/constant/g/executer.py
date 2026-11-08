from ..abstractConstantExecuter import abstractConstantExecuter


class g(abstractConstantExecuter):
    """
    Configures the gravity vector ('g') in OpenFOAM, defining the direction and magnitude of gravitational acceleration.

    Usage:
        Provide the gravity vector as a 3-component list (x, y, z), typically specifying acceleration in m/s².

    Example:
        Setting gravity to [0, 0, -9.81] to simulate standard Earth gravity acting in the negative Z direction.
    """

    def __init__(self,JSON):
        super().__init__(JSON,"g")
