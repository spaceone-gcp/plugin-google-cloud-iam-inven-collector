import json
import logging

from plugin.connector import GoogleCloudConnector

__all__ = ["CloudRunV2Connector"]

_LOGGER = logging.getLogger("spaceone")


class CloudRunV2Connector(GoogleCloudConnector):
    google_client_service = "run"
    version = "v2"

    def list_services(self, parent: str) -> list:
        """
        Cloud Run 서비스 목록을 조회합니다.
        
        Args:
            parent: 프로젝트 리소스 경로 (projects/{project_id}/locations/{location})
            
        Returns:
            Cloud Run 서비스 목록
        """
        try:
            request = self.client.projects().locations().services().list(parent=parent)
            response = request.execute()
            _LOGGER.info(f"Services found: {json.dumps(response.get('services', []))}")
            return response.get('services', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list Cloud Run services: {str(e)}")
            return []

    def list_revisions(self, parent: str) -> list:
        """
        Cloud Run 리비전 목록을 조회합니다.
        
        Args:
            parent: 서비스 리소스 경로 (projects/{project_id}/locations/{location}/services/{service_id})
            
        Returns:
            Cloud Run 리비전 목록
        """
        try:
            request = self.client.projects().locations().services().revisions().list(parent=parent)
            response = request.execute()
            _LOGGER.info(f"Revisions found: {json.dumps(response.get('revisions', []))}")
            return response.get('revisions', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list Cloud Run revisions: {str(e)}")
            return []

    def list_jobs(self, parent: str) -> list:
        """
        Cloud Run Jobs 목록을 조회합니다.
        
        Args:
            parent: 프로젝트 리소스 경로 (projects/{project_id}/locations/{location})
            
        Returns:
            Cloud Run Jobs 목록
        """
        try:
            request = self.client.projects().locations().jobs().list(parent=parent)
            response = request.execute()
            _LOGGER.info(f"Jobs found: {json.dumps(response.get('jobs', []))}")
            return response.get('jobs', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list Cloud Run jobs: {str(e)}")
            return []

    def list_executions(self, parent: str) -> list:
        """
        Cloud Run Job Executions 목록을 조회합니다.
        
        Args:
            parent: Job 리소스 경로 (projects/{project_id}/locations/{location}/jobs/{job_id})
            
        Returns:
            Cloud Run Job Executions 목록
        """
        try:
            request = self.client.projects().locations().jobs().executions().list(parent=parent)
            response = request.execute()
            _LOGGER.info(f"Executions found: {json.dumps(response.get('executions', []))}")
            return response.get('executions', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list Cloud Run executions: {str(e)}")
            return []

    def list_tasks(self, parent: str) -> list:
        """
        Cloud Run Job Execution Tasks 목록을 조회합니다.
        
        Args:
            parent: Execution 리소스 경로 (projects/{project_id}/locations/{location}/jobs/{job_id}/executions/{execution_id})
            
        Returns:
            Cloud Run Job Execution Tasks 목록
        """
        try:
            request = self.client.projects().locations().jobs().executions().tasks().list(parent=parent)
            response = request.execute()
            _LOGGER.info(f"Tasks found: {json.dumps(response.get('tasks', []))}")
            return response.get('tasks', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list Cloud Run tasks: {str(e)}")
            return []

    def list_worker_pools(self, parent: str) -> list:
        """
        Cloud Run Worker Pools 목록을 조회합니다.
        
        Args:
            parent: 프로젝트 리소스 경로 (projects/{project_id}/locations/{location})
            
        Returns:
            Cloud Run Worker Pools 목록
        """
        try:
            request = self.client.projects().locations().workerPools().list(parent=parent)
            response = request.execute()
            _LOGGER.info(f"Worker Pools found: {json.dumps(response.get('workerPools', []))}")
            return response.get('workerPools', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list Cloud Run worker pools: {str(e)}")
            return []

    def list_worker_pool_revisions(self, parent: str) -> list:
        """
        Cloud Run Worker Pool Revisions 목록을 조회합니다.
        
        Args:
            parent: Worker Pool 리소스 경로 (projects/{project_id}/locations/{location}/workerPools/{worker_pool_id})
            
        Returns:
            Cloud Run Worker Pool Revisions 목록
        """
        try:
            request = self.client.projects().locations().workerPools().revisions().list(parent=parent)
            response = request.execute()
            _LOGGER.info(f"Worker Pool Revisions found: {json.dumps(response.get('revisions', []))}")
            return response.get('revisions', [])
        except Exception as e:
            _LOGGER.error(f"Failed to list Cloud Run worker pool revisions: {str(e)}")
            return []