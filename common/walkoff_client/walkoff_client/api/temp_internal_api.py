# coding: utf-8

"""
    WALKOFF

    An active cyber defense development framework enabling orchestration capabilities to be written once and deployed across WALKOFF-enabled orchestration tools. https://nsacyber.github.io/WALKOFF/  # noqa: E501

    The version of the OpenAPI document: 0.9.1
    Contact: walkoff@nsa.gov
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from walkoff_client.api_client import ApiClient
from walkoff_client.exceptions import (
    ApiTypeError,
    ApiValueError
)


class TempInternalApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def update_workflow_status(self, execution_id, event, json_patch, **kwargs):  # noqa: E501
        """Patch parts of a WorkflowStatusMessage object  # noqa: E501

        For internal use only. This endpoint should only be available to the docker network.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_workflow_status(execution_id, event, json_patch, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str execution_id: execution_id of workflow status to update (required)
        :param str event: The event type that is being submitted (required)
        :param JSONPatch json_patch: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: WorkflowStatus
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.update_workflow_status_with_http_info(execution_id, event, json_patch, **kwargs)  # noqa: E501

    def update_workflow_status_with_http_info(self, execution_id, event, json_patch, **kwargs):  # noqa: E501
        """Patch parts of a WorkflowStatusMessage object  # noqa: E501

        For internal use only. This endpoint should only be available to the docker network.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_workflow_status_with_http_info(execution_id, event, json_patch, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str execution_id: execution_id of workflow status to update (required)
        :param str event: The event type that is being submitted (required)
        :param JSONPatch json_patch: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(WorkflowStatus, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['execution_id', 'event', 'json_patch']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_workflow_status" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'execution_id' is set
        if ('execution_id' not in local_var_params or
                local_var_params['execution_id'] is None):
            raise ApiValueError("Missing the required parameter `execution_id` when calling `update_workflow_status`")  # noqa: E501
        # verify the required parameter 'event' is set
        if ('event' not in local_var_params or
                local_var_params['event'] is None):
            raise ApiValueError("Missing the required parameter `event` when calling `update_workflow_status`")  # noqa: E501
        # verify the required parameter 'json_patch' is set
        if ('json_patch' not in local_var_params or
                local_var_params['json_patch'] is None):
            raise ApiValueError("Missing the required parameter `json_patch` when calling `update_workflow_status`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'execution_id' in local_var_params:
            path_params['execution_id'] = local_var_params['execution_id']  # noqa: E501

        query_params = []
        if 'event' in local_var_params:
            query_params.append(('event', local_var_params['event']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'json_patch' in local_var_params:
            body_params = local_var_params['json_patch']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/internal/workflowstatus/{execution_id}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WorkflowStatus',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)