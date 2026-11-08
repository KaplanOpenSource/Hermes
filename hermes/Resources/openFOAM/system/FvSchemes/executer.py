from ....general import JinjaTransform


class FvSchemes(JinjaTransform):
    """
    Configures the 'fvSchemes' file in OpenFOAM, which defines the numerical discretization schemes for gradients, divergence, and Laplacian terms.

    Usage:
        Choose between different interpolation schemes (e.g., upwind, linear) to balance simulation stability and accuracy.

    Example:
        Using a second-order upwind scheme for the convection term to achieve higher spatial accuracy in high-velocity flow regions.
    """

    pass