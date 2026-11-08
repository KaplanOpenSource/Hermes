from ....general import JinjaTransform


class physicalProperties(JinjaTransform):
    """
    Configures the 'physicalProperties' file in OpenFOAM, defining key constants such as density and other material-specific properties.

    Usage:
        Provide the fluid properties required for the simulation, such as a constant value for density.

    Example:
        Specifying the density of air at 15°C to ensure accurate pressure and flow calculations in an atmospheric dispersion model.
    """

    pass
