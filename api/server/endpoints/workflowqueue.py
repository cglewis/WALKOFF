import datetime
import json
import uuid
from http import HTTPStatus
import logging
from datetime import datetime

from typing import List

from starlette.requests import Request
from pydantic import ValidationError
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import HTTPException

from api.server.db.permissions import auth_check
from api.server.db.workflow import WorkflowModel
from common.config import static
from common.message_types import StatusEnum, message_dumps
from api.server.db import get_mongo_d, get_mongo_c
from api.server.db.workflowresults import WorkflowStatus, ExecuteWorkflow, ControlWorkflow
from api.server.security import get_jwt_claims, get_jwt_identity
from api.server.endpoints.results import push_to_workflow_stream_queue
from api.server.utils.problems import InvalidInputException, ImproperJSONException, DoesNotExistException
from common.redis_helpers import connect_to_aioredis_pool
from common.config import config
from common.mongo_helpers import get_item, create_item

router = APIRouter()
logger = logging.getLogger(__name__)


# def workflow_status_getter(execution_id, app_api_col: AsyncIOMotorCollection):
# return await app_api_col.find_one({"execution_id": execution_id}, projection={'_id': False})


# def workflow_getter(workflow_id, app_api_col: AsyncIOMotorCollection):
#     return await app_api_col.find_one({"workflow_id": workflow_id}, projection={'_id': False})


# status_order = OrderedDict(
#     [((StatusEnum.EXECUTING, StatusEnum.AWAITING_DATA, StatusEnum.PAUSED),
#       WorkflowStatus.started_at),
#      ((StatusEnum.ABORTED, StatusEnum.COMPLETED), WorkflowStatus.completed_at)])
#
# executing_statuses = (StatusEnum.EXECUTING, StatusEnum.AWAITING_DATA, StatusEnum.PAUSED)
# completed_statuses = (StatusEnum.ABORTED, StatusEnum.COMPLETED)


@router.get("/",
            response_model=List[WorkflowStatus],
            response_description="List of status information of all workflows currently executing.",
            status_code=200)
async def get_all_workflow_status(request: Request, workflow_status_col: AsyncIOMotorCollection = Depends(get_mongo_c)):
    """
    Returns a list of status information of workflows currently executing WALKOFF.
    """
    walkoff_db = get_mongo_d(request)
    workflow_col = walkoff_db.workflows
    curr_user_id = await get_jwt_identity(request)

    temp = []
    ret = []
    for wf_status in (await workflow_status_col.find().to_list(None)):
        temp.append(WorkflowStatus(**wf_status))

    for wf_status in temp:
        id = wf_status.workflow_id
        wf = await get_item(workflow_col, WorkflowModel, id)
        to_read = await auth_check(wf, curr_user_id, "read", walkoff_db=walkoff_db)
        if to_read:
            ret.append(wf_status)

    return ret


@router.get("/{execution}",
            response_model=WorkflowStatus,
            response_description="Returns status information of a workflow specified by execution ID.",
            status_code=200)
async def get_workflow_status(request: Request, execution,
                              workflow_status_col: AsyncIOMotorCollection = Depends(get_mongo_c)):
    """
    Returns status information of a workflow currently executing WALKOFF.
    """
    walkoff_db = get_mongo_d(request)
    workflow_col = walkoff_db.workflows
    curr_user_id = await get_jwt_identity(request)
    workflow_status = await get_item(workflow_status_col, WorkflowStatus, execution)
    # workflow_status = workflow_status_getter(execution, workflow_status_col)
    wf = await get_item(workflow_col, WorkflowModel, workflow_status.workflow_id)

    to_read = await auth_check(wf, curr_user_id, "read", walkoff_db=walkoff_db)
    if to_read:
        return workflow_status
    else:
        return None


@router.post("/",
             response_model=dict,
             response_description="Execute a workflow.",
             status_code=202)
async def execute_workflow(workflow_to_execute: ExecuteWorkflow, request: Request,
                           workflow_status_col: AsyncIOMotorCollection = Depends(get_mongo_c)):
    """
    Executes a WALKOFF workflow.
    """
    walkoff_db = get_mongo_d(request)
    workflow_col = walkoff_db.workflows

    workflow_id = workflow_to_execute.workflow_id
    execution_id = workflow_to_execute.execution_id
    workflow: WorkflowModel = await get_item(workflow_col, WorkflowModel, workflow_id)
    # workflow = workflow_getter(workflow_id, workflow_status_col)
    # data = dict(workflow_to_execute)

    curr_user_id = await get_jwt_identity(request)

    to_execute = await auth_check(workflow, curr_user_id, "execute", walkoff_db=walkoff_db)
    if to_execute:
        if not workflow:
            raise DoesNotExistException("workflow", "execute", workflow_id)

        if not workflow.is_valid:
            raise InvalidInputException("workflow", "execute", workflow.id_, errors=workflow.errors)

        # workflow = dict(workflow)

        actions_by_id = {a.id_: a for a in workflow.actions}
        triggers_by_id = {t.id_: t for t in workflow.triggers}

        # TODO: Add validation to all overrides
        if "start" in workflow_to_execute:
            if workflow_to_execute.start in actions_by_id or workflow_to_execute.start in triggers_by_id:
                workflow.start = workflow_to_execute.start
            else:
                raise InvalidInputException("execute", "workflow", workflow.id_,
                                            errors=["Start override must be an action or a trigger in this workflow."])

        if "workflow_variables" in workflow and "workflow_variables" in workflow_to_execute:
            # TODO: change these on the db model to be keyed by ID
            # Get workflow variables keyed by ID

            current_wvs = {wv.id_: wv for wv in workflow.workflow_variables}
            new_wvs = {wv['id_']: wv for wv in workflow_to_execute.workflow_variables}

            # Update workflow variables with new values, ignore ids that didn't already exist
            override_wvs = {id_: new_wvs[id_] if id_ in new_wvs else current_wvs[id_] for id_ in current_wvs}
            workflow.workflow_variables = list(override_wvs.values())

        if "parameters" in workflow_to_execute:
            if workflow_to_execute.start is not None:
                start_id = workflow_to_execute.start
            else:
                start_id = workflow.start
            # start_id = data.get("start", workflow.start)
            if start_id in actions_by_id:
                parameters_by_name = {p.name: p for p in actions_by_id[start_id].parameters}
                for parameter in workflow_to_execute.parameters:
                    parameters_by_name[parameter.name] = parameter
                actions_by_id[start_id].parameters = list(parameters_by_name.values())
                workflow.actions = list(actions_by_id.values())
            else:
                raise InvalidInputException("workflow", "execute", workflow.id_,
                                            errors=["Cannot override starting parameters for anything but an action."])

        try:
            # TODO: add check for workflow_col VALIDATION
            execution_id = await execute_workflow_helper(request=request, workflow_id=workflow_id,
                                                         workflow_col=workflow_col, execution_id=execution_id,
                                                         workflow=workflow, workflow_status_col=workflow_status_col)
            return {'execution_id': execution_id}
        except ValidationError as e:
            raise ImproperJSONException('workflow_status', 'create', workflow.name, e)
            # raise e.messages
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


async def execute_workflow_helper(request: Request, workflow_id, workflow_status_col: AsyncIOMotorCollection,
                                  workflow_col: AsyncIOMotorCollection = None, execution_id=None,
                                  workflow: WorkflowModel = None):
    if not execution_id:
        execution_id = str(uuid.uuid4())
    if not workflow:
        workflow = await get_item(workflow_col, WorkflowModel, workflow_id)

    workflow_status_json = {  # ToDo: Probably load this directly into db model?
        "execution_id": execution_id,
        "workflow_id": workflow_id,
        "name": workflow.name,
        "status": StatusEnum.PENDING.name,
        "started_at": str(datetime.now().isoformat()),
        # "completed_at": None,
        "user": (await get_jwt_claims(request)).get('username', None),
        "node_status": [],
        # "app_name": None,
        # "action_name": None,
        # "label": None
    }
    workflow_status = WorkflowStatus(**workflow_status_json)
    await create_item(workflow_status_col, WorkflowStatus, workflow_status)
    # Assign the execution id to the workflow so the worker knows it
    workflow.execution_id = execution_id
    # ToDo: self.__box.encrypt(message))
    async with connect_to_aioredis_pool(config.REDIS_URI) as conn:
        await conn.sadd(static.REDIS_PENDING_WORKFLOWS, str(execution_id))
        await conn.xadd(static.REDIS_WORKFLOW_QUEUE, {str(execution_id): workflow.json()})
    workflow_status.status = StatusEnum.PENDING
    await push_to_workflow_stream_queue(workflow_status, "PENDING")
    logger.info(f"Created Workflow Status {workflow.name} ({execution_id})")

    return execution_id


@router.patch("/{execution}",
              response_model=str,
              response_description="Pause, resume, or abort a workflow.",
              status_code=204)
async def control_workflow(request: Request, execution, workflow_to_control: ControlWorkflow,
                           workflow_status_col: AsyncIOMotorCollection = Depends(get_mongo_c)):
    """
    Pause, resume, or abort a workflow currently executing in WALKOFF.
    """
    walkoff_db = get_mongo_d(request)
    workflow_col = walkoff_db.workflows
    curr_user_id = await get_jwt_identity(request)

    workflow_id = execution.workflow_id
    data = dict(workflow_to_control)
    status = data['status']

    workflow: WorkflowModel = await get_item(workflow_col, WorkflowModel, workflow_id)
    # workflow = workflow_getter(execution.workflow_id, workflow_status_col)
    # The resource factory returns the WorkflowStatus model but we want the string of the execution ID
    execution_id = str(execution.execution_id)

    to_execute = await auth_check(workflow, curr_user_id, "execute", walkoff_db=walkoff_db)
    # TODO: add in pause/resume here. Workers need to store and recover state for this
    if to_execute:
        if status == 'abort':
            logger.info(
                f"User '{(await get_jwt_claims(request)).get('username', None)}' aborting workflow: {execution_id}")
            message = {"execution_id": execution_id, "status": status, "workflow": dict(workflow)}
            async with connect_to_aioredis_pool(config.REDIS_URI) as conn:
                await conn.smove(static.REDIS_PENDING_WORKFLOWS,
                                 static.REDIS_ABORTING_WORKFLOWS, execution_id)
                await conn.xadd(static.REDIS_WORKFLOW_CONTROL, message)

            return None, HTTPStatus.NO_CONTENT
        elif status == 'trigger':
            if execution.status not in (StatusEnum.PENDING, StatusEnum.EXECUTING, StatusEnum.AWAITING_DATA):
                raise InvalidInputException("workflow", "trigger", execution_id,
                                            errors=["Workflow must be in a running state to accept triggers."])

            trigger_id = data.get('trigger_id')
            if not trigger_id:
                raise InvalidInputException("workflow", "trigger", execution_id,
                                            errors=["ID of the trigger must be specified in trigger_id."])
            seen = False
            for trigger in workflow.triggers:
                if str(trigger.id_) == trigger_id:
                    seen = True

            if not seen:
                raise InvalidInputException("workflow", "trigger", execution_id,
                                            errors=[f"trigger_id {trigger_id} was not found in this workflow."])

            trigger_stream = f"{execution_id}-{trigger_id}:triggers"

            try:
                async with connect_to_aioredis_pool(config.REDIS_URI) as conn:
                    info = await conn.xinfo_stream(trigger_stream)
                stream_length = info["length"]
            except Exception:
                stream_length = 0

            if stream_length > 0:
                return InvalidInputException("workflow", "trigger", execution_id,
                                             errors=[f"This trigger has already received data."])

            trigger_data = data.get('trigger_data')
            logger.info(
                f"User '{(await get_jwt_claims(request)).get('username', None)}' triggering workflow: {execution_id} at trigger "
                f"{trigger_id} with data {trigger_data}")
            async with connect_to_aioredis_pool(config.REDIS_URI) as conn:
                await conn.xadd(trigger_stream, {execution_id: message_dumps({"trigger_data": trigger_data})})

            return ({"trigger_stream": trigger_stream})
    else:
        return None


@router.delete("/cleardb",
               response_model=str,
               response_description="Removes workflow statuses from the execution database. It will delete all of them or ones older than a certain number of days",
               status_code=204)
# ToDo: make these clear db endpoints for more resources
async def clear_workflow_status(all_=False, days=30,
                                workflow_status_col: AsyncIOMotorCollection = Depends(get_mongo_c)):
    """
    Removes workflow statuses from the execution database."
    """
    if all_:
        await workflow_status_col.remove({"$or":
                                              [{"status": StatusEnum.ABORTED}, {"status": StatusEnum.COMPLETED}]},
                                         projection={'_id': False})
    elif days > 0:
        delete_date = datetime.datetime.today() - datetime.timedelta(days=days)
        temp = await workflow_status_col.find({"$or":
                                                   [{"status": StatusEnum.ABORTED}, {"status": StatusEnum.COMPLETED}]},
                                              projection={'_id': False})
        temp2 = await workflow_status_col.find({"completed_at": {"$lte": delete_date}},
                                               projection={'_id': False})

        to_delete = list((set(temp)).intersection(set(temp2)))
        await workflow_status_col.deleteMany(to_delete)
    return None
