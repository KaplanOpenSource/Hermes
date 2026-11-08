from ..abstractSystemExecuter import abstractSystemExecuter


class CreatePatch(abstractSystemExecuter):
    """
    Configures the 'createPatch' utility to define and organize boundary patches in an OpenFOAM mesh.

    Usage:
        Define which faces should be grouped into specific patches (e.g., 'inlet', 'outlet', 'walls') based on their location or surface characteristics.

    Example:
        Creating a dedicated patch for a pollutant source area so that custom boundary conditions can be applied specifically to that region.
    """

    pass
    # def __init__(self,JSON):
    #     super().__init__(JSON,"CreatePatch")
