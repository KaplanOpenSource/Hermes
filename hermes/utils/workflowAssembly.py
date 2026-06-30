from hermes import expandWorkflow,workflow
import json
import os
import pathlib
import shutil
import logging
import uuid
from ..utils.jsonutils import loadJSON


# Luigi scheduler selection used by buildLuigiExecutionCommand below.
SCHEDULER_LOCAL = "local"
SCHEDULER_CENTRAL = "central"


def buildLuigiExecutionCommand(moduleName, scheduler=SCHEDULER_LOCAL,
                               schedulerHost=None, schedulerPort=None,
                               targetTask="finalnode_xx_0"):
    """Build the ``python3 -m luigi`` command line used to execute a workflow.

    ``scheduler="local"`` (default) adds ``--local-scheduler``; ``"central"`` connects
    to a running ``luigid`` (optionally at ``schedulerHost``/``schedulerPort``, otherwise
    Luigi's defaults).
    """
    cmd = f"python3 -m luigi --module {moduleName} {targetTask}"
    if scheduler == SCHEDULER_CENTRAL:
        if schedulerHost is not None:
            cmd += f" --scheduler-host {schedulerHost}"
        if schedulerPort is not None:
            cmd += f" --scheduler-port {schedulerPort}"
    else:
        cmd += " --local-scheduler"
    return cmd

def handler_expand(arguments):
    logger = logging.getLogger("hermes.bin.expand")
    logger.info("---------- Start ---------")

    exapnder = expandWorkflow()

    templateFileName = f"{arguments.workflow.split('.')[0]}.json"
    expandedWorkflow = f"{arguments.caseName.split('.')[0]}.json"

    logger.debug(f"Expanding {templateFileName} to {expandedWorkflow}")
    newTemplate = exapnder.expandBatch(templateJSON=templateFileName)

    logger.debug(f"Writing the expanded workflow to {expandedWorkflow}")
    with open(expandedWorkflow, 'w') as fp:
        json.dump(newTemplate, fp,indent=4)

    logger.info("---------- End ---------")

def handler_build(arguments):
    logger = logging.getLogger("hermes.bin.build")
    logger.info("---------- Start ---------")
    handler_expand(arguments)

    templateFileName = f"{arguments.workflow.split('.')[0]}.json"
    newTemplate = loadJSON(templateFileName)
    newWorkflow = f"{arguments.caseName.split('.')[0]}.py"

    WDPath = os.getcwd()
    builder = "luigi"
    flow = workflow(newTemplate, WDPath)
    build = flow.build(builder)
    with open(newWorkflow, "w") as file:
        file.write(build)

def handler_execute(arguments):
    """
        Executes the built workflow with the selected Luigi scheduler.

        The scheduler (local/central), its optional host/port and the dispatch_id are
        read from ``arguments`` (falling back to the local scheduler and a fresh uuid4
        when not provided), so the centralized scheduler can tell distinct runs apart.
    :param arguments:
    :return:
    """

    pythonPath = arguments.caseName.split(".")[0]

    scheduler = getattr(arguments, "scheduler", SCHEDULER_LOCAL) or SCHEDULER_LOCAL
    schedulerHost = getattr(arguments, "scheduler_host", None)
    schedulerPort = getattr(arguments, "scheduler_port", None)
    dispatch_id = getattr(arguments, "dispatch_id", None) or uuid.uuid4().hex

    #cwd = pathlib.Path().absolute()
    #moduleParent = pathlib.Path(pythonPath).parent.absolute()
    #os.chdir(moduleParent)
    executionStr = buildLuigiExecutionCommand(os.path.basename(pythonPath), dispatch_id,
                                              scheduler=scheduler, schedulerHost=schedulerHost,
                                              schedulerPort=schedulerPort)
    print(executionStr)

    if arguments.force:
        # delete the run files if exist.
        executionfileDir = f"{arguments.caseName.split('.')[0]}_targetFiles"
        shutil.rmtree(executionfileDir, ignore_errors=True)

    os.system(executionStr)


    #os.chdir(cwd)


def handler_buildExecute(arguments):
    logger = logging.getLogger("hermes.bin")
    logger.info("---------- Start ---------")
    arguments.caseName = arguments.workflow

    if not arguments.force:
        # check if there is old expanded json, or python.
        # also if there are old runfiles it will not rerun.

        expnded = f"{arguments.caseName.split('.')[0]}.json"
        newWorkflow = f"{arguments.caseName.split('.')[0]}.py"

        if os.path.exists(newWorkflow):
            print(f"Python execution file {newWorkflow} exists. Delete or run with --force flag.")
            exit()

    logger.debug(f"Expanding the workflow with arguments {arguments}")
    handler_expand(arguments)
    arguments.workflow = arguments.caseName
    arguments.parameters = None
    logger.debug(f"building the workflow with arguments {arguments}")
    handler_build(arguments)

    if arguments.force:

        # delete the run files if exist.
        executionfileDir = f"{arguments.caseName.split('.')[0]}_targetFiles"
        logger.debug(f"Got remove, tree, deleting {executionfileDir}")
        shutil.rmtree(executionfileDir, ignore_errors=True)

    logger.debug("Executing the workflow")
    handler_execute(arguments)
    logger.info("----------- End ----------")
