from ....general import JinjaTransform


class BlockMesh(JinjaTransform):
    """
    Generates the 'blockMeshDict' file in OpenFOAM to create a basic structured mesh consisting of rectangular blocks.

    Usage:
        Define the vertices and block structure (how points are connected) that form the geometry of your simulation domain.

    Example:
        Creating a simple cubic region for a wind tunnel simulation before further refining it with more complex tools.
    """

    pass