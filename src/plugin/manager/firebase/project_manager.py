import logging
from typing import Generator

from spaceone.inventory.plugin.collector.lib import make_cloud_service

from plugin.connector.firebase_connector import FirebaseConnector
from plugin.manager.base import ResourceManager

_LOGGER = logging.getLogger("spaceone")


class FirebaseProjectManager(ResourceManager):
    service = "Firebase"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Firebase"
        self.cloud_service_type = "Project"
        self.service_code = None
        self.is_primary = True
        self.icon = "firebase.svg"
        self.labels = []
        self.metadata_path = "metadata/firebase_project.yaml"
        self.firebase_connector = None

    def collect_cloud_services(
        self, options: dict, secret_data: dict, schema: str
    ) -> Generator[dict, None, None]:
        try:
            _LOGGER.debug(f"[{self.__repr__()}] Initializing Firebase connector")
            self.firebase_connector = FirebaseConnector(options, secret_data, schema)

            # Firebase 프로젝트 목록 조회
            _LOGGER.debug(f"[{self.__repr__()}] Fetching Firebase projects")
            projects = self.get_all_firebase_projects()
            _LOGGER.debug(
                f"[{self.__repr__()}] Found {len(projects)} Firebase projects"
            )

            for project in projects:
                yield self.make_cloud_service_info(project, secret_data)

        except Exception as e:
            _LOGGER.error(
                f"[{self.__repr__()}] Error collecting Firebase projects: {str(e)}",
                exc_info=True,
            )
            raise

    def get_all_firebase_projects(self) -> list:
        """
        모든 Firebase 프로젝트를 페이지네이션을 통해 조회합니다.

        Returns:
            list: Firebase 프로젝트 목록
        """
        try:
            all_projects = []
            page_token = None

            while True:
                response = self.firebase_connector.list_available_projects(
                    page_token=page_token, page_size=100
                )

                # response가 dict인지 확인
                if isinstance(response, dict):
                    projects = response.get("results", [])
                    all_projects.extend(projects)

                    # 다음 페이지가 있는지 확인
                    page_token = response.get("nextPageToken")
                    if not page_token:
                        break
                else:
                    # response가 dict가 아닌 경우 (에러 핸들러에서 빈 리스트 반환)
                    _LOGGER.warning(
                        f"[{self.__repr__()}] Unexpected response type: {type(response)}"
                    )
                    break

            return all_projects

        except Exception as e:
            _LOGGER.error(
                f"[{self.__repr__()}] Error fetching Firebase projects: {str(e)}"
            )
            return []

    def make_cloud_service_info(self, project: dict, secret_data: dict) -> dict:
        """
        Firebase 프로젝트 정보를 SpaceONE 클라우드 서비스 형식으로 변환합니다.

        Args:
            project (dict): Firebase 프로젝트 정보

        Returns:
            dict: SpaceONE 클라우드 서비스 정보
        """
        project_id = project.get("projectId")
        display_name = project.get("displayName")
        project_number = project.get("projectNumber")
        state = project.get("state", "UNKNOWN")

        # 프로젝트 상태에 따른 상태 매핑
        if state == "ACTIVE":
            status = "ACTIVE"
        elif state == "DELETED":
            status = "DELETED"
        else:
            status = "UNKNOWN"

        # 리소스 정보 구성
        resource_data = {
            "projectId": project_id,
            "displayName": display_name,
            "projectNumber": project_number,
            "state": state,
            "status": status,
            "name": project.get("name"),
            "etag": project.get("etag"),
            "annotations": project.get("annotations", {}),
        }

        # 태그 정보 구성
        tags = []
        if display_name:
            tags.append({"key": "DisplayName", "value": display_name})
        if project_number:
            tags.append({"key": "ProjectNumber", "value": str(project_number)})
        if state:
            tags.append({"key": "State", "value": state})

        return make_cloud_service(
            name=display_name or project_id,
            cloud_service_type=self.cloud_service_type,
            cloud_service_group=self.cloud_service_group,
            provider=self.provider,
            data=resource_data,
            account=secret_data.get("project_id"),
            tags=tags,
            region_code="global",
            reference={
                "resource_id": project_id,
                "external_link": f"https://console.firebase.google.com/project/{project_id}",
            },
        )
