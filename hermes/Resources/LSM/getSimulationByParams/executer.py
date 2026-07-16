from ...executers.abstractExecuter import abstractExecuter


class getSimulationByParams(abstractExecuter):
    """
        Runs a Fortran LSM simulation.

        inputs:
            ProjectName : str, The class path string to the class
            Template : str, The class path string to the class
            SimulationParameters : str, The class path string to the class
            SimulationName : str, The class path string to the class
    """

    def _defaultParameters(self):
        return dict(
            output=[],

            inputs=["ProjectName","Template", "SimulationParameters", "SimulationName"],
            # possible_simulation_params = ['TopoFile', 'flat', 'TopoXmin', 'TopoXmax', 'TopoYmin', 'TopoYmax', 'TopoXn', 'TopoYn', 'sourceRatioX', 'sourceRatioY', 'releaseDuration', 'releaseHeight', 'windSpeed', 'windDir', 'inversionHeight', 'savedt', 'duration', 'nParticles', 'savedx', 'savedy', 'savedz', 'StationsFile', 'homogeneousWind', 'particles3D', 'wind3D', 'n_vdep', 'lineSource', 'stability']
            webGUI={},
            parameters={}
        )

    def run(self, **inputs):
        self.logger.info("Starting LSM simulation")

        from hera import toolkitHome
        from hera.datalayer import Project
        from hera.utils.jsonutils import JSONToConfiguration


        if 'ProjectName' not in inputs:
            raise Exception("Node wasn't given project name through `ProjectName` parameter")
        p = Project(projectName=inputs['ProjectName'])


        if 'SimulationName' not in inputs:
            raise Exception("Node wasn't given simulation name through `SimulationName` parameter")
        simulation_name = inputs['SimulationName']
        
        template = inputs.get("Template", "v4-general")

        old_lsm_toolkit = toolkitHome.getToolkit(toolkitName=toolkitHome.LSM, projectName=p.projectName, to_xarray=True, to_database=False, forceKeep=True)

        lsm_templates = old_lsm_toolkit.getTemplates(template=template)
        if len(lsm_templates) == 0:
            raise Exception("Template v4-general isn't loaded to the project. Please load the relevant repository for v4-general into the project.")
        lsm_template = lsm_templates[0]

        sim_params = inputs.get('SimulationParameters', {})
        sim_params = JSONToConfiguration(sim_params)
        if sim_params == {}:
            self.logger.info("Simulation parameters were not specified, running default template parameters")

        res = lsm_template.getSimulation(simulation_name=simulation_name, **sim_params)

        return dict(runSimulation="runSimulation",dosageXarray=res.xarray_path)