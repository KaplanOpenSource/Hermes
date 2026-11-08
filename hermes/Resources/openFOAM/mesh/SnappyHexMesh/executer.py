from ....general import JinjaTransform


class SnappyHexMesh(JinjaTransform):
    """
    Configures 'snappyHexMeshDict' to create complex, unstructured meshes that conform to detailed surface geometries.

    Usage:
        Define the background mesh (from blockMesh) and provide surface files; configure settings for casting, snapping, and layering to refine the mesh around surfaces.

    Example:
        Creating a highly accurate mesh around the curved surfaces of a vehicle to capture precise airflow patterns.
    """

    pass