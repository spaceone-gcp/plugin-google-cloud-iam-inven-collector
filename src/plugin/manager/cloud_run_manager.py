import logging
from typing import Generator

from spaceone.inventory.plugin.collector.lib import make_cloud_service

from plugin.connector.cloud_run_v1_connector import CloudRunV1Connector
from plugin.connector.cloud_run_v2_connector import CloudRunV2Connector
from plugin.manager.base import ResourceManager

_LOGGER = logging.getLogger("spaceone")


class CloudRunManager(ResourceManager):
    service = "CloudRun"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "CloudRun"
        self.cloud_service_type = "Service"
        self.service_code = None
        self.is_primary = False
        self.icon = "cloud_run.svg"
        self.labels = []
        self.metadata_path = "metadata/cloud_run.yaml" # TODO: 메타데이터 파일 추가 필요
        self.cloud_run_v1_connector = None
        self.cloud_run_v2_connector = None

    def collect_cloud_services(
        self, options: dict, secret_data: dict, schema: str
    ) -> Generator[dict, None, None]:
        self.cloud_run_v1_connector = CloudRunV1Connector(options, secret_data, schema)
        self.cloud_run_v2_connector = CloudRunV2Connector(options, secret_data, schema)
        project_id = secret_data.get("project_id")

        # Cloud Run v1 API를 사용하여 location 목록 조회
        locations = self.cloud_run_v1_connector.list_locations()
        location_ids = [location.get('locationId') for location in locations if location.get('locationId')]
        
        # 각 location에서 Cloud Run 리소스들 조회
        for location_id in location_ids:
            parent = f"projects/{project_id}/locations/{location_id}"
            
            try:                
                # 1. Cloud Run v2 Services 조회
                services = self.cloud_run_v2_connector.list_services(parent)
                if services:
                    _LOGGER.debug(f"Found {len(services)} services in {location_id}")
                    for service in services:
                        # 1.1. 각 Service의 Revisions 조회
                        service_name = service.get("name")
                        if service_name:
                            revisions = self.cloud_run_v2_connector.list_revisions(service_name)
                            service["revisions"] = revisions
                            service["revision_count"] = len(revisions)
                        
                        # TODO : yield 로 변경
                        # yield self.make_cloud_run_resource_info(service, project_id, location_id, "Service")
                        _LOGGER.debug(f"service: {self.make_cloud_run_resource_info(service, project_id, location_id, 'Service')}")
                
                # 2. Cloud Run v2 Jobs 조회
                jobs = self.cloud_run_v2_connector.list_jobs(parent)
                if jobs:
                    _LOGGER.debug(f"Found {len(jobs)} jobs in {location_id}")
                    for job in jobs:
                        # 각 Job의 Executions 정보도 조회
                        job_name = job.get("name")
                        if job_name:
                            executions = self.cloud_run_v2_connector.list_executions(job_name)
                            job["executions"] = executions
                            job["execution_count"] = len(executions)
                            
                            # 각 Execution의 Tasks 정보도 조회
                            for execution in executions:
                                execution_name = execution.get("name")
                                if execution_name:
                                    tasks = self.cloud_run_v2_connector.list_tasks(execution_name)
                                    execution["tasks"] = tasks
                                    execution["task_count"] = len(tasks)
                        
                        # TODO : yield 로 변경
                        # yield self.make_cloud_run_resource_info(job, project_id, location_id, "Job")
                        _LOGGER.debug(f"job: {self.make_cloud_run_resource_info(job, project_id, location_id, 'Job')}")
                
                # 3. Cloud Run Worker Pools 조회
                worker_pools = self.cloud_run_v2_connector.list_worker_pools(parent)
                if worker_pools:
                    _LOGGER.debug(f"Found {len(worker_pools)} worker pools in {location_id}")
                    for worker_pool in worker_pools:
                        # 각 Worker Pool의 Revisions 정보도 조회
                        worker_pool_name = worker_pool.get("name")
                        if worker_pool_name:
                            revisions = self.cloud_run_v2_connector.list_worker_pool_revisions(worker_pool_name)
                            worker_pool["revisions"] = revisions
                            worker_pool["revision_count"] = len(revisions)
                        
                        # TODO : yield 로 변경
                        # yield self.make_cloud_run_resource_info(worker_pool, project_id, location_id, "WorkerPool")
                        _LOGGER.debug(f"worker_pool: {self.make_cloud_run_resource_info(worker_pool, project_id, location_id, 'WorkerPool')}")
                        
            except Exception as e:
                # 특정 location에서 API 호출이 실패해도 다른 location은 계속 확인
                _LOGGER.debug(f"Failed to query {location_id}: {str(e)}")
                continue

    def make_cloud_run_resource_info(
        self, resource: dict, project_id: str, location_id: str, resource_type: str
    ) -> dict:
        """
        Cloud Run 리소스 정보를 생성하는 제네릭 메소드
        
        Args:
            resource: 리소스 데이터
            project_id: 프로젝트 ID
            location_id: 리전 ID
            resource_type: 리소스 타입 (Service, Job, WorkerPool)
        """
        # 리소스 타입별 설정
        resource_configs = {
            "Service": {
                "external_link_path": f"https://console.cloud.google.com/run/detail/{location_id}/{{name}}?project={project_id}"
            },
            "Job": {
                "external_link_path": f"https://console.cloud.google.com/run/jobs/{{name}}?project={project_id}"
            },
            "WorkerPool": {
                "external_link_path": f"https://console.cloud.google.com/run/worker-pools/{{name}}?project={project_id}"
            }
        }
        
        config = resource_configs.get(resource_type, {})
        resource_name = resource.get("name", "")
        resource_id = resource.get("uid", "")
        
        # external link 생성
        external_link = config.get("external_link_path", "").format(name=resource_name)
        
        return make_cloud_service(
            name=resource_name,
            cloud_service_type=resource_type,
            cloud_service_group=self.cloud_service_group,
            provider=self.provider,
            account=f"projects/{project_id}",
            data=resource,
            region_code=location_id,
            reference={
                "resource_id": resource_id,
                "external_link": external_link
            }
        )
    
