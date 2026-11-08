from ..abstractDispersionExecuter import abstractDispersionExecuter


class KinematicCloudProperties(abstractDispersionExecuter):
    """
    Configures the 'kinematicCloudProperties' file in OpenFOAM, defining the physical properties of particles or droplets in a Lagrangian cloud simulation.

    Usage:
        Specify particle characteristics such as diameter, density, and interaction models (e.g., drag, gravity).

    Example:
        Defining the size and weight of aerosol particles to simulate how they settle over time due to gravity versus being carried by the wind.
    """

    def __init__(self,JSON):
        super().__init__(JSON,"KinematicCloudProperties")
