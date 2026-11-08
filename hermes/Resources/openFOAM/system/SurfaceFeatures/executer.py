from ..abstractSystemExecuter import abstractSystemExecuter


class SurfaceFeatures(abstractSystemExecuter):
    """
    Configures the 'surfaceFeatures' utility to extract important geometric features (edges) from an STL surface file.

    Usage:
        Provide the path to the STL file and specify the extraction angle; these features are then used by snappyHexMesh to ensure sharp edges are preserved in the final mesh.

    Example:
        Extracting the crisp corners of a building model to prevent them from being smoothed over during the snapping process in snappyHexMesh.
    """

    pass
    # def __init__(self,JSON):
    #     super().__init__(JSON,"SurfaceFeatures")



