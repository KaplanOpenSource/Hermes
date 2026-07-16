from ...executers.abstractExecuter import abstractExecuter


class runSimulation(abstractExecuter):
    """
        Runs a Fortran LSM simulation.

        inputs:
            ProjectName : str, The class path string to the class
            Template : str, The class path string to the class
            SimulationParameters : str, The class path string to the class
            SimulationName : str, The class path string to the class
            saveMode : str, The class path string to the class
            topography : str, The class path string to the class
            stations : str, The class path string to the class
            canopy  : str, The name of the function to run .
            depositionRates : dict, The parameters for the function.
    """

    def _defaultParameters(self):
        return dict(
            output=[],

            inputs=["ProjectName","LSMDosagePath", "policy"],
            webGUI={},
            parameters={}
        )

    def run(self, **inputs):
        self.logger.info("Starting LSM simulation")

        if 'ProjectName' not in inputs:
            raise Exception("Node wasn't given project name through `ProjectName` parameter")
        if 'LSMDosagePath' not in inputs:
            raise Exception("Node wasn't given LSM simulation results path through `LSMPath` parameter")
        if 'policy' not in inputs:
            raise Exception("Node wasn't given the protection policy through `policy` parameter")

        from uuid import uuid4

        import hera.datalayer
        from hera.datalayer.autocache import cacheFunction
        from hera.riskassessment import ProtectionPolicy
        from hera.simulations.LSM.singleSimulation import SingleSimulation

        p = hera.datalayer.Project(projectName=inputs['ProjectName'])
        s = SingleSimulation(inputs['LSMDosagePath'])

        
        policy = ProtectionPolicy()

        policy_dict = inputs['policy']
        if not isinstance(policy_dict , dict):
            raise Exception("Protection policy must be dictionary of applied policies in the order of execution")
        
        policy.addActions([{"name": policy_name, "params":{policy_desc}} for policy_name, policy_desc in policy_dict.items()])

        uuid = str(uuid4())

        @cacheFunction(returnFormat=hera.datalayer.datatypes.NETCDF_XARRAY, projectName=p.projectName)
        def policyComputeCache(_):
            return policy.compute(s.getConcentration(), C="C")
        
        policyComputeCache(uuid)
        docs = p.getCacheDocuments(type="functionCacheData", functionName=policyComputeCache.__name__, uuid=[True, uuid])
        if len(docs) == 0:
            raise Exception("The policy wasn't saved, aborting")
        elif len(docs) > 1:
            raise Exception(f"There is more than one policy saved with the UUID {uuid}, aborting")
        doc = docs[0]
        return dict(createPythonClass="createPythonClass",concentrationXarray=doc.resource)