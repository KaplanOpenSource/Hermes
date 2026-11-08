from ..abstractSystemExecuter import abstractSystemExecuter


class MeshQualityDict(abstractSystemExecuter):
    """
    Configures the 'meshQualityDict' file in OpenFOAM, defining the thresholds used to evaluate the quality of the simulation mesh.

    Usage:
        Set limits for metrics such as non-orthogonality and skewness to ensure the mesh is suitable for stable numerical calculations.

    Example:
        Defining a maximum allowable non-orthogonality threshold to alert the user if certain cells are too distorted, which could lead to convergence issues.
    """

    pass
    # def __init__(self,JSON):
    #     super().__init__(JSON,"MeshQualityDict")