import json
import logging

from plugin.connector import GoogleCloudConnector

__all__ = ["CloudRunV1Connector"]

_LOGGER = logging.getLogger("spaceone")


class CloudRunV1Connector(GoogleCloudConnector):
    google_client_service = "run"
    version = "v1"

    def list_locations(self) -> list:
        """
        Cloud Run에서 지원하는 모든 location 목록을 조회합니다.
        
        Returns:
            Cloud Run location 목록
        """
        try:
            request = self.client.projects().locations().list(name=f"projects/{self.project_id}")
            response = request.execute()
            _LOGGER.info(f"Locations found: {json.dumps(response.get('locations', []))}")
            return response.get('locations', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list locations from Cloud Run API: {str(e)}")
            return []

    def list_domain_mappings(self, parent: str) -> list:
        """
        Cloud Run v1 도메인 매핑 목록을 조회합니다.
        
        Args:
            parent: 프로젝트 리소스 경로 (projects/{project_id}/locations/{location})
            
        Returns:
            Cloud Run v1 도메인 매핑 목록
        """
        try:
            request = self.client.projects().locations().domainmappings().list(parent=parent)
            response = request.execute()
            _LOGGER.info(f"Domain mappings found: {json.dumps(response.get('items', []))}")
            return response.get('items', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list Cloud Run v1 domain mappings: {str(e)}")
            return []

