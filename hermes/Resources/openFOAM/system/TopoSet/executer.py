from ....general import JinjaTransform


class TopoSet(JinjaTransform):
    """
    Configures the 'topoSet' utility to create sets of cells, faces, or points based on geometric or logical criteria.

    Usage:
        Define rules for membership in a set (e.g., all cells within a certain distance from a point), which can then be used by other tools like refineMesh or setFields.

    Example:
        Creating a set of all cells within 10 meters of a pollutant source to specifically apply a higher resolution mesh in that area.
    """

    pass