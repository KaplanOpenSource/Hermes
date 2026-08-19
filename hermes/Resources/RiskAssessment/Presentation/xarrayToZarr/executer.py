from ....executers.abstractExecuter import abstractExecuter


class xarrayToZarr(abstractExecuter):
    """
    Converts an Xarray Dataset/DataArray to a zarr file.

    inputs:
        Xarray : str, path to an Xarray file or serialized lazy Xarray/Dask tree
        OutputPath : str, path where the zarr file should be written
    """

    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=["Xarray", "OutputPath"],
            webGUI={},
            parameters={}
        )

    @staticmethod
    def testParamValues(params: dict[str, any]):
        passed, status_message = abstractExecuter.checkParamType(
            params, "Xarray", str, required=True
        )
        if not passed:
            return passed, status_message

        passed, status_message = abstractExecuter.checkParamType(
            params, "OutputPath", str, required=True
        )
        if not passed:
            return passed, status_message

        return True, ""

    def run(self, **inputs):
        """
        Converts an Xarray Dataset/DataArray to a zarr file.

        If the input is a serialized lazy Xarray/Dask tree, it is
        materialized before being converted to zarr.
        """

        if 'Xarray' not in inputs:
            raise Exception(
                "Node wasn't given an Xarray through the `Xarray` parameter"
            )

        if 'OutputPath' not in inputs:
            raise Exception(
                "Node wasn't given an output path through the `OutputPath` parameter"
            )
        output_path = inputs['OutputPath']

        xarr, is_lazy = self.load_xarray(inputs['Xarray'])

        xarr.to_zarr(output_path)

        return dict(
            zarrPath=output_path
        )