# walkoff-client
An active cyber defense development framework enabling orchestration capabilities to be written once and deployed across WALKOFF-enabled orchestration tools. https://nsacyber.github.io/WALKOFF/

This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 0.9.1
- Package version: 1.0.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

Clone the Repo, then cd to the client and pip install it
```sh
git clone https://github.com/nsacyber/WALKOFF.git
cd WALKOFF/common/walkoff_client
pip install .
```

Then import the package:
```python
import walkoff_client 
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then try the following to create an example workflow and run it:

```python
import urllib3
from time import sleep

import walkoff_client as walkoff


def main():
    # Create a config that represents our Walkoff server
    config = walkoff.Configuration(host="https://192.168.56.101:8080/api")

    # Since Walkoff uses a self-signed certificate, we need to disable certificate verification
    config.verify_ssl = False
    config.ssl_ca_cert = None
    config.assert_hostname = False
    config.cert_file = None
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Create a base API client with which you will interact with Walkoff
    api_client = walkoff.ApiClient(configuration=config)

    # Create an authentication API client and log in
    auth_api = walkoff.AuthorizationApi(api_client)
    tokens = auth_api.login(walkoff.Authentication(username="admin", password="admin"))
    config.access_token = tokens.access_token

    # Create a workflow API client and perform your desired actions
    workflow_api = walkoff.WorkflowsApi(api_client)
    r = workflow_api.read_all_workflows()
    print(r)

    workflow = {
        "_walkoff_type": "workflow",
        "actions": [
            {
                "_walkoff_type": "action",
                "app_name": "hello_world",
                "app_version": "1.0.0",
                "errors": [],
                "id_": "0871a04e-9caf-6ebe-8c18-3efd016fd304",
                "is_valid": True,
                "label": "repeat_back_to_me",
                "name": "repeat_back_to_me",
                "parallelized": False,
                "parameters": [
                    {
                        "_walkoff_type": "parameter",
                        "id_": "0becfa01-5e1a-49c1-981f-2d94b7e839bd",
                        "name": "call",
                        "parallelized": False,
                        "value": "examplevalue",
                        "variant": "STATIC_VALUE"
                    }
                ],
                "position": {
                    "_walkoff_type": "position",
                    "x": 290,
                    "y": 390
                },
                "priority": 3
            }
        ],
        "id_": "abad0f4b-5965-fc5d-b3d5-dcf0c1f61a8d",
        "name": "ExampleWorkflow",
        "start": "0871a04e-9caf-6ebe-8c18-3efd016fd304",
    }

    r2 = workflow_api.create_workflow(workflow)

    print(r2)

    assert len(workflow_api.read_all_workflows()) == 1

    wfq_task = walkoff.ExecuteWorkflow(parameters=[{
        "_walkoff_type": "parameter",
        "id_": "0becfa01-5e1a-49c1-981f-2d94b7e839bd",
        "name": "call",
        "parallelized": False,
        "value": "overriding value",
        "variant": "STATIC_VALUE"
    }], workflow_id=workflow["id_"])

    workflowqueue_api = walkoff.WorkflowQueueApi(api_client)

    workflowqueue_api.execute_workflow(wfq_task)


if __name__ == "__main__":
    main()

```

## Documentation for API Endpoints

All URIs are relative to *http://\<hostname\>/api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AppsApi* | [**create_app_api**](docs/AppsApi.md#create_app_api) | **POST** /apps/apis | Create app api
*AppsApi* | [**delete_app_api**](docs/AppsApi.md#delete_app_api) | **DELETE** /apps/apis/{app} | Delete app api
*AppsApi* | [**read_all_app_apis**](docs/AppsApi.md#read_all_app_apis) | **GET** /apps/apis | Get all app apis
*AppsApi* | [**read_app_api**](docs/AppsApi.md#read_app_api) | **GET** /apps/apis/{app} | Get and app&#39;s api
*AppsApi* | [**update_app_api**](docs/AppsApi.md#update_app_api) | **PUT** /apps/apis/{app} | Replace app api
*AuthorizationApi* | [**login**](docs/AuthorizationApi.md#login) | **POST** /auth | Login and get access and refresh tokens
*AuthorizationApi* | [**logout**](docs/AuthorizationApi.md#logout) | **POST** /auth/logout | Logout of walkoff
*AuthorizationApi* | [**refresh**](docs/AuthorizationApi.md#refresh) | **POST** /auth/refresh | Get a fresh access token
*DashboardsApi* | [**create_dashboard**](docs/DashboardsApi.md#create_dashboard) | **POST** /dashboards | Create a dashboard
*DashboardsApi* | [**delete_dashboard**](docs/DashboardsApi.md#delete_dashboard) | **DELETE** /dashboards/{dashboard} | Delete a dashboard
*DashboardsApi* | [**read_all_dashboards**](docs/DashboardsApi.md#read_all_dashboards) | **GET** /dashboards | Read all dashboards
*DashboardsApi* | [**read_dashboard**](docs/DashboardsApi.md#read_dashboard) | **GET** /dashboards/{dashboard} | Get a dashboard by id
*DashboardsApi* | [**update_dashboard**](docs/DashboardsApi.md#update_dashboard) | **PUT** /dashboards | Update a dashboard
*GlobalVariablesApi* | [**create_global**](docs/GlobalVariablesApi.md#create_global) | **POST** /globals | Add a global
*GlobalVariablesApi* | [**create_global_templates**](docs/GlobalVariablesApi.md#create_global_templates) | **POST** /globals/templates | Add a global
*GlobalVariablesApi* | [**delete_global**](docs/GlobalVariablesApi.md#delete_global) | **DELETE** /globals/{global_var} | Remove a global
*GlobalVariablesApi* | [**delete_global_templates**](docs/GlobalVariablesApi.md#delete_global_templates) | **DELETE** /globals/templates/{global_template} | Remove a global
*GlobalVariablesApi* | [**read_all_global_templates**](docs/GlobalVariablesApi.md#read_all_global_templates) | **GET** /globals/templates | Get all global templates
*GlobalVariablesApi* | [**read_all_globals**](docs/GlobalVariablesApi.md#read_all_globals) | **GET** /globals | Get all globals
*GlobalVariablesApi* | [**read_global**](docs/GlobalVariablesApi.md#read_global) | **GET** /globals/{global_var} | Read a global
*GlobalVariablesApi* | [**read_global_templates**](docs/GlobalVariablesApi.md#read_global_templates) | **GET** /globals/templates/{global_template} | Read a global template
*GlobalVariablesApi* | [**update_global**](docs/GlobalVariablesApi.md#update_global) | **PUT** /globals/{global_var} | Update a global
*GlobalVariablesApi* | [**update_global_templates**](docs/GlobalVariablesApi.md#update_global_templates) | **PUT** /globals/templates/{global_template} | Update a global template
*RolesApi* | [**create_role**](docs/RolesApi.md#create_role) | **POST** /roles | Create a role
*RolesApi* | [**delete_role**](docs/RolesApi.md#delete_role) | **DELETE** /roles/{role_id} | Delete a role
*RolesApi* | [**read_all_roles**](docs/RolesApi.md#read_all_roles) | **GET** /roles | Read all roles
*RolesApi* | [**read_available_resource_actions**](docs/RolesApi.md#read_available_resource_actions) | **GET** /availableresourceactions | Read all available resource actions
*RolesApi* | [**read_role**](docs/RolesApi.md#read_role) | **GET** /roles/{role_id} | Read a role
*RolesApi* | [**update_role**](docs/RolesApi.md#update_role) | **PUT** /roles/{role_id} | Update a role
*SchedulerApi* | [**create_scheduled_task**](docs/SchedulerApi.md#create_scheduled_task) | **POST** /scheduledtasks | Create a new Scheduled Task
*SchedulerApi* | [**delete_scheduled_task**](docs/SchedulerApi.md#delete_scheduled_task) | **DELETE** /scheduledtasks/{scheduled_task_id} | Delete the scheduled task
*SchedulerApi* | [**get_scheduler_status**](docs/SchedulerApi.md#get_scheduler_status) | **GET** /scheduler | Get the current scheduler status.
*SchedulerApi* | [**read_all_scheduled_tasks**](docs/SchedulerApi.md#read_all_scheduled_tasks) | **GET** /scheduledtasks | Get all the scheduled tasks
*SchedulerApi* | [**read_scheduled_task**](docs/SchedulerApi.md#read_scheduled_task) | **GET** /scheduledtasks/{scheduled_task_id} | Get the scheduled task
*SchedulerApi* | [**update_scheduled_task**](docs/SchedulerApi.md#update_scheduled_task) | **PUT** /scheduledtasks/{scheduled_task_id} | Update a new Scheduled Task
*SchedulerApi* | [**update_scheduler_status**](docs/SchedulerApi.md#update_scheduler_status) | **PUT** /scheduler | Update the status of the scheduler
*SettingsApi* | [**read_settings**](docs/SettingsApi.md#read_settings) | **GET** /settings | Reads the settings
*SettingsApi* | [**update_settings**](docs/SettingsApi.md#update_settings) | **PUT** /settings | Updates the settings
*SystemApi* | [**read_all_app_names**](docs/SystemApi.md#read_all_app_names) | **GET** /apps | Gets all apps
*TempInternalApi* | [**update_workflow_status**](docs/TempInternalApi.md#update_workflow_status) | **PATCH** /internal/workflowstatus/{execution_id} | Patch parts of a WorkflowStatusMessage object
*UsersApi* | [**create_user**](docs/UsersApi.md#create_user) | **POST** /users | Create a user
*UsersApi* | [**delete_user**](docs/UsersApi.md#delete_user) | **DELETE** /users/{user_id} | Delete a user
*UsersApi* | [**read_all_users**](docs/UsersApi.md#read_all_users) | **GET** /users | Read all users
*UsersApi* | [**read_user**](docs/UsersApi.md#read_user) | **GET** /users/{user_id} | Get a user
*UsersApi* | [**update_user**](docs/UsersApi.md#update_user) | **PUT** /users/{user_id} | Update a user
*WorkflowQueueApi* | [**clear_workflow_status**](docs/WorkflowQueueApi.md#clear_workflow_status) | **DELETE** /workflowqueue/cleardb | Removes workflow statuses from the execution database. It will delete all of them or ones older than a certain number of days
*WorkflowQueueApi* | [**control_workflow**](docs/WorkflowQueueApi.md#control_workflow) | **PATCH** /workflowqueue/{execution} | Abort or trigger a workflow
*WorkflowQueueApi* | [**execute_workflow**](docs/WorkflowQueueApi.md#execute_workflow) | **POST** /workflowqueue | Execute a workflow
*WorkflowQueueApi* | [**get_all_workflow_status**](docs/WorkflowQueueApi.md#get_all_workflow_status) | **GET** /workflowqueue | Get status information on the workflows currently executing
*WorkflowQueueApi* | [**get_workflow_status**](docs/WorkflowQueueApi.md#get_workflow_status) | **GET** /workflowqueue/{execution} | Get status information on a currently executing workflow
*WorkflowsApi* | [**create_workflow**](docs/WorkflowsApi.md#create_workflow) | **POST** /workflows | Create a workflow
*WorkflowsApi* | [**delete_workflow**](docs/WorkflowsApi.md#delete_workflow) | **DELETE** /workflows/{workflow} | Delete a workflow
*WorkflowsApi* | [**read_all_workflows**](docs/WorkflowsApi.md#read_all_workflows) | **GET** /workflows | Read all workflows in playbook
*WorkflowsApi* | [**read_workflow**](docs/WorkflowsApi.md#read_workflow) | **GET** /workflows/{workflow} | Read a workflow
*WorkflowsApi* | [**update_workflow**](docs/WorkflowsApi.md#update_workflow) | **PUT** /workflows/{workflow} | Update a workflow


## Documentation For Models

 - [Action](docs/Action.md)
 - [ActionApi](docs/ActionApi.md)
 - [AddResource](docs/AddResource.md)
 - [AddRole](docs/AddRole.md)
 - [AddScheduledTask](docs/AddScheduledTask.md)
 - [AddUser](docs/AddUser.md)
 - [ApiContact](docs/ApiContact.md)
 - [ApiLicense](docs/ApiLicense.md)
 - [ApiTag](docs/ApiTag.md)
 - [AppApi](docs/AppApi.md)
 - [Authentication](docs/Authentication.md)
 - [AvailableResourceAction](docs/AvailableResourceAction.md)
 - [AvailableSubscriptions](docs/AvailableSubscriptions.md)
 - [Branch](docs/Branch.md)
 - [Condition](docs/Condition.md)
 - [ControlWorkflow](docs/ControlWorkflow.md)
 - [CopyWorkflow](docs/CopyWorkflow.md)
 - [Dashboard](docs/Dashboard.md)
 - [DisplayUser](docs/DisplayUser.md)
 - [EditUser](docs/EditUser.md)
 - [Error](docs/Error.md)
 - [ExecuteWorkflow](docs/ExecuteWorkflow.md)
 - [ExternalDoc](docs/ExternalDoc.md)
 - [GlobalVariable](docs/GlobalVariable.md)
 - [GlobalVariableTemplate](docs/GlobalVariableTemplate.md)
 - [InlineObject](docs/InlineObject.md)
 - [InlineObject1](docs/InlineObject1.md)
 - [InlineResponse200](docs/InlineResponse200.md)
 - [InlineResponse2001](docs/InlineResponse2001.md)
 - [InlineResponse2002](docs/InlineResponse2002.md)
 - [JSONPatch](docs/JSONPatch.md)
 - [NodeStatus](docs/NodeStatus.md)
 - [NodeStatusSummary](docs/NodeStatusSummary.md)
 - [Parameter](docs/Parameter.md)
 - [ParameterApi](docs/ParameterApi.md)
 - [ParameterSchema](docs/ParameterSchema.md)
 - [Position](docs/Position.md)
 - [Resource](docs/Resource.md)
 - [ReturnApi](docs/ReturnApi.md)
 - [Role](docs/Role.md)
 - [ScheduledTask](docs/ScheduledTask.md)
 - [Scheduler](docs/Scheduler.md)
 - [Settings](docs/Settings.md)
 - [TaskTrigger](docs/TaskTrigger.md)
 - [Token](docs/Token.md)
 - [Transform](docs/Transform.md)
 - [Trigger](docs/Trigger.md)
 - [Widget](docs/Widget.md)
 - [WorkflowJSON](docs/WorkflowJSON.md)
 - [WorkflowMetaData](docs/WorkflowMetaData.md)
 - [WorkflowStatus](docs/WorkflowStatus.md)
 - [WorkflowStatusSummary](docs/WorkflowStatusSummary.md)
 - [WorkflowVariable](docs/WorkflowVariable.md)


## Documentation For Authorization


## AuthenticationToken

- **Type**: Bearer authentication (JWT)


## Author

walkoff@nsa.gov

