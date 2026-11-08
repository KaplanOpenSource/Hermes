from ....general import JinjaTransform


class FvConstraints(JinjaTransform):
    """
    Configures the finite volume (FV) constraints in OpenFOAM, defining additional mathematical or physical restrictions on the solved fields.

    Usage:
        Specify any required numerical constraints or source terms that must be applied globally or locally across the simulation domain.

    Example:
        Adding a constraint to ensure that concentration values never drop below zero during a dispersion simulation, preventing numerical instabilities.
    """

    pass
