from ..abstractSystemExecuter import abstractSystemExecuter


class DecomposePar(abstractSystemExecuter):
    """
    Configures the 'decomposePar' utility to split a simulation domain into multiple sub-domains for parallel execution on a cluster.

    Usage:
        Specify how the mesh should be decomposed (e.g., simple, hierarchical) and the number of processors to use.

    Example:
        Splitting a large urban area mesh across 64 CPU cores to reduce simulation time from days to hours.
    """
    pass
    # def __init__(self,JSON):
    #     super().__init__(JSON,"DecomposePar")
