import logging
import os

import magic
import xarray

from ...executers.abstractExecuter import abstractExecuter


class runProtectionPolicy(abstractExecuter):
    """
        Runs a Fortran LSM simulation.

        inputs:
            ProjectName : str, The class path string to the class
            LSMDosagePath : str, path to file containing the dosage used in policy protection calculation
            LSMConcentrationPath : str, path to file containing the concentration used in policy protection calculation
            policy : dict, dictionary of the policies to be applied
    """

    def _defaultParameters(self):
        return dict(
            output=[],

            inputs=["ProjectName","LSMDosagePath", "LSMConcentrationPath", "policy"],
            webGUI={},
            parameters={}
        )

    def run(self, **inputs):

        if 'ProjectName' not in inputs:
            raise Exception("Node wasn't given project name through `ProjectName` parameter")
        if 'policy' not in inputs:
            raise Exception("Node wasn't given the protection policy through `policy` parameter")

        from hera.datalayer import Project
        from hera.riskassessment import ProtectionPolicy
        from hera.simulations.LSM.singleSimulation import SingleSimulation

        p = Project(projectName=inputs['ProjectName'])
        if 'LSMDosagePath' in inputs:
            pickled_xarray, is_pickle = self.load_xarray(inputs["LSMDosagePath"])

            conc = SingleSimulation(pickled_xarray if is_pickle else inputs['LSMDosagePath']).getConcentration()
        elif 'LSMConcentrationPath' not in inputs:
            pickled_xarray, is_pickle = self.load_xarray(inputs["LSMConcentrationPath"])
            if is_pickle:
                conc = pickled_xarray
            else:
                conc = xarray.open_mfdataset(inputs["LSMConcentrationPath"], combine='by_coords')
        else:
            raise Exception("Node wasn't given LSM simulation results path through `LSMConcentrationPath` or `LSMDosagePath` parameter")

        
        policy = ProtectionPolicy()

        policy_dict = inputs['policy']
        if not isinstance(policy_dict , dict):
            raise Exception("Protection policy must be dictionary of applied policies in the order of execution")
        
        policy.addActions({"actions":[{"name": policy_name, "params":policy_desc} for policy_name, policy_desc in policy_dict.items()]})

        res = policy.compute(conc, C="C", lazy=True)
        return dict(runProtectionPolicy="runProtectionPolicy",concentrationXarray=str(self.save_dask_tree(project=p, dask_tree=res)))