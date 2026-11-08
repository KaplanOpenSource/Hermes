from ....general import JinjaTransform


class FvSolution(JinjaTransform):
    """
    Configures the 'fvSolution' file in OpenFOAM, which specifies the linear solvers, preconditioners, and convergence tolerances for each variable.

    Usage:
        Select appropriate solvers (e.g., GAMG for pressure, PBiCGStab for velocity) and set the relative tolerance to ensure a converged solution.

    Example:
        Optimizing solver settings to reduce computation time while ensuring that the residuals for momentum and continuity drop below 1e-6.
    """

    pass
