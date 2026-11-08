from ..abstractDispersionExecuter import abstractDispersionExecuter


class IndoorDict(abstractDispersionExecuter):
    """
    Configures the dispersion parameters for indoor environments, accounting for confined spaces and internal ventilation.

    Usage:
        Specify boundary conditions and source terms tailored for room-scale or building-scale airflow and pollutant transport.

    Example:
        Simulating the spread of a contaminant within an office space to evaluate the effectiveness of the HVAC system in removing the agent.
    """

    def __init__(self,JSON):
        super().__init__(JSON,"IndoorDict")
