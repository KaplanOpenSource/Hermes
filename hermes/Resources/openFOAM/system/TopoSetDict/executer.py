from ....general import JinjaTransform


class TopoSetDict(JinjaTransform):
    """
    Generates the 'topoSetDict' file used by the topoSet utility to define set membership rules.

    Usage:
        Specify the target sets and the criteria (e.g., box, cylinder, or face-based) for selecting elements in the mesh.

    Example:
        Defining a cylindrical region around a chimney stack so that it can be identified as a specific set for later post-processing analysis.
    """

    pass