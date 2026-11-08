from ..abstractConstantExecuter import abstractConstantExecuter


class ThermophysicalProperties(abstractConstantExecuter):
    """
    Configures the 'thermophysicalProperties' file in OpenFOAM, which defines the thermodynamic and physical properties of the materials used in the simulation.

    Usage:
        Specify the fluid type, transport model, and thermophysical models (e.g., constant heat capacity).

    Example:
        Setting up a simulation for air at standard temperature and pressure by defining its specific heat and thermal conductivity.
    """

    def __init__(self,JSON):
        super().__init__(JSON,"ThermophysicalProperties")
