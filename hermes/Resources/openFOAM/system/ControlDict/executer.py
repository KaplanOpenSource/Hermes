from ..abstractSystemExecuter import abstractSystemExecuter

class ControlDict(abstractSystemExecuter):
    """
    Configures the 'controlDict' file, which acts as the main control center for an OpenFOAM simulation.

    Usage:
        Set the start and end times of the simulation, the time step (deltaT), and how often to write result files to disk.

    Example:
        Running a simulation from 0 to 100 seconds with a time step of 0.1 seconds, saving results every 10 seconds.
    """

    pass
    #
    # def __init__(self,JSON):
    #     super().__init__(JSON,"ControlDict")