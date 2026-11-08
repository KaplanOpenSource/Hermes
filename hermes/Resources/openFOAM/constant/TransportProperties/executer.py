from ..abstractConstantExecuter import abstractConstantExecuter


class TransportProperties(abstractConstantExecuter):
    """
    Configures the 'transportProperties' file in OpenFOAM, which controls fluid transport coefficients such as kinematic viscosity and diffusion coefficients.

    Usage:
        Define the transport model (e.g., constant) and provide the values for parameters like nu (viscosity).

    Example:
        Setting the viscosity of water to ensure the correct Reynolds number is achieved in a flow simulation.
    """


    def __init__(self,JSON):
        super().__init__(JSON,"TransportProperties")
