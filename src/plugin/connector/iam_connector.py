import logging

from spaceone.core import cache

from plugin.connector import GoogleCloudConnector
from plugin.utils.error_handlers import api_retry_handler

__all__ = ["IAMConnector"]

_LOGGER = logging.getLogger("spaceone")


class IAMConnector(GoogleCloudConnector):
    google_client_service = "iam"
    version = "v1"

    @api_retry_handler(default_response=[])
    def list_service_accounts(self, project_id: str = None) -> list:
        project_id = project_id or self.project_id
        service_accounts = []

        query = {"name": f"projects/{project_id}", "pageSize": 100}
        request = self.client.projects().serviceAccounts().list(**query)

        while True:
            response = request.execute()
            service_accounts.extend(response.get("accounts", []))
            request = (
                self.client.projects()
                .serviceAccounts()
                .list_next(previous_request=request, previous_response=response)
            )

            if request is None:
                break

        return service_accounts

    @api_retry_handler(default_response=[])
    def list_service_account_keys(
        self, service_account_email: str, project_id: str = None
    ):
        project_id = project_id or self.project_id
        ## 리팩토링 3 : gcp 서비스 계정 키 조회 API 호출 시 필터 추가하여 조회 ("keyTypes": ["USER_MANAGED"])
        query = {
            "name": f"projects/{project_id}/serviceAccounts/{service_account_email}",
            "keyTypes": ["USER_MANAGED"],
        }
        request = self.client.projects().serviceAccounts().keys().list(**query)
        response = request.execute()

        return response.get("keys", [])

    @api_retry_handler(default_response=[])
    def query_testable_permissions(self, resource: str):
        body = {"fullResourceName": resource}
        permissions = []

        while True:
            request = self.client.permissions().queryTestablePermissions(body=body)
            response = request.execute()
            permissions.extend(response.get("permissions", []))

            if "nextPageToken" not in response:
                break

            body["pageToken"] = response["nextPageToken"]

        return permissions

    ## 리팩토링 3-1 : 인자로 showDeleted=True 추가하여 삭제된 역할도 조회 가능하도록 수정
    @api_retry_handler(default_response=[])
    def list_project_roles(self, project_id: str = None, show_deleted=False):
        parent = f"projects/{project_id}"
        roles = []
        request = (
            self.client.projects()
            .roles()
            .list(parent=parent, pageSize=1000, view="FULL", showDeleted=show_deleted)
        )

        while True:
            response = request.execute()

            roles.extend(response.get("roles", []))

            request = (
                self.client.projects()
                .roles()
                .list_next(previous_request=request, previous_response=response)
            )

            if request is None:
                break

        return roles

    ## 리팩토링 3-1 : 인자로 showDeleted=True 추가하여 삭제된 역할도 조회 가능하도록 수정
    @api_retry_handler(default_response=[])
    def list_organization_roles(self, resource, show_deleted=False):
        roles = []
        request = (
            self.client.organizations()
            .roles()
            .list(parent=resource, pageSize=1000, view="FULL", showDeleted=show_deleted)
        )

        while True:
            response = request.execute()
            roles.extend(response.get("roles", []))

            request = (
                self.client.organizations()
                .roles()
                .list_next(previous_request=request, previous_response=response)
            )

            if request is None:
                break

        return roles

    @api_retry_handler(default_response=[])
    def list_roles(self):
        roles = []
        request = self.client.roles().list(pageSize=1000, view="FULL")
        while True:
            response = request.execute()
            roles.extend(response.get("roles", []))

            request = self.client.roles().list_next(
                previous_request=request, previous_response=response
            )

            if request is None:
                break

        return roles

    @api_retry_handler(default_response={})
    @cache.cacheable(key="plugin:connector:role:{name}", alias="local")
    def get_role(self, name: str):
        return self.client.roles().get(name=name).execute()
