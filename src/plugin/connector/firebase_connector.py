import logging

from plugin.connector import GoogleCloudConnector
from plugin.utils.error_handlers import api_retry_handler

__all__ = ["FirebaseConnector"]

_LOGGER = logging.getLogger("spaceone")


class FirebaseConnector(GoogleCloudConnector):
    google_client_service = "firebase"
    version = "v1beta1"

    @api_retry_handler(default_response=[])
    def list_available_projects(
        self, page_token: str = None, page_size: int = None, show_deleted: bool = None
    ) -> dict:
        """
        Firebase Management API의 availableProjects 엔드포인트를 호출하여 사용 가능한 프로젝트 목록을 반환합니다.

        Args:
            page_token (str, optional): 페이지네이션을 위한 토큰
            page_size (int, optional): 한 번에 반환할 프로젝트 수
            show_deleted (bool, optional): 삭제된 프로젝트도 포함할지 여부

        Returns:
            dict: Firebase 프로젝트 목록과 다음 페이지 토큰
        """
        query_params = {}

        if page_token:
            query_params["pageToken"] = page_token
        if page_size:
            query_params["pageSize"] = page_size
        if show_deleted is not None:
            query_params["showDeleted"] = show_deleted

        # Firebase Management API의 projects 엔드포인트 사용
        request = self.client.projects().list(**query_params)
        response = request.execute()

        return response

    @api_retry_handler(default_response=[])
    def get_project(self, project_id: str) -> dict:
        """
        특정 Firebase 프로젝트의 상세 정보를 반환합니다.

        Args:
            project_id (str): Firebase 프로젝트 ID

        Returns:
            dict: Firebase 프로젝트 정보
        """
        request = self.client.projects().get(name=f"projects/{project_id}")
        response = request.execute()

        return response
