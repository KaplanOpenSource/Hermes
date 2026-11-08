from ..abstractSystemExecuter import abstractSystemExecuter


class ChangeDictionary(abstractSystemExecuter):
    """
    Configures the 'changeDictionary' utility in OpenFOAM to modify existing dictionary files without rewriting them from scratch.

    Usage:
        Specify which entries in a target dictionary should be changed, added, or removed.

    Example:
        Updating the boundary conditions of a specific patch in 'U' (velocity) file after the mesh has been generated.
    """

    pass
    # def __init__(self,JSON):
    #     super().__init__(JSON,"ChangeDictionary")

