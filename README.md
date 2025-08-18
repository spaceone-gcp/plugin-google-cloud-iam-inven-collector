# plugin-google-cloud-iam-inven-collector

Google Cloud IAM 및 Firebase 리소스를 수집하는 SpaceONE 플러그인입니다.

## 지원하는 리소스

### IAM 리소스
- **Service Account**: 서비스 계정 정보 및 키 관리
- **Role**: IAM 역할 (사전 정의, 조직, 프로젝트 레벨)
- **Permission**: IAM 권한 정보
- **Group**: Cloud Identity 그룹 정보

### Firebase 리소스
- **Project**: Firebase 프로젝트 정보

## Firebase Management API 지원

이 플러그인은 Firebase Management API v1beta1을 사용하여 Firebase 프로젝트 정보를 수집합니다.

### 지원하는 Firebase API 엔드포인트
- `GET /v1beta1/availableProjects`: 사용 가능한 Firebase 프로젝트 목록 조회
- `GET /v1beta1/projects/{projectId}`: 특정 Firebase 프로젝트 상세 정보 조회

### Firebase 프로젝트 수집 기능
- Firebase 프로젝트 목록 조회 (페이지네이션 지원)
- 프로젝트 상태별 필터링 (ACTIVE, DELETED)
- 프로젝트 메타데이터 수집 (프로젝트 ID, 표시 이름, 프로젝트 번호 등)

## 설치 및 설정

### 필수 권한
Firebase 프로젝트를 수집하려면 다음 권한이 필요합니다:
- `https://www.googleapis.com/auth/firebase`
- `https://www.googleapis.com/auth/firebase.readonly`

### 환경 변수 설정
테스트를 위해 다음 환경 변수를 설정하세요:
```bash
export GOOGLE_CLOUD_TYPE="service_account"
export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
export GOOGLE_CLOUD_PRIVATE_KEY_ID="your-private-key-id"
export GOOGLE_CLOUD_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
export GOOGLE_CLOUD_CLIENT_EMAIL="your-service-account@your-project.iam.gserviceaccount.com"
export GOOGLE_CLOUD_CLIENT_ID="your-client-id"
export GOOGLE_CLOUD_AUTH_URI="https://accounts.google.com/o/oauth2/auth"
export GOOGLE_CLOUD_TOKEN_URI="https://oauth2.googleapis.com/token"
export GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
export GOOGLE_CLOUD_CLIENT_X509_CERT_URL="https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

## 테스트

Firebase 커넥터를 테스트하려면:
```bash
python test_firebase_connector.py
```

## 구조

```
src/plugin/
├── connector/
│   ├── firebase_connector.py          # Firebase Management API 커넥터
│   └── ...
├── manager/
│   ├── firebase/
│   │   ├── __init__.py
│   │   └── project_manager.py         # Firebase 프로젝트 매니저
│   └── ...
├── metadata/
│   └── firebase_project.yaml          # Firebase 프로젝트 메타데이터
└── metrics/
    └── Firebase/
        └── Project/
            ├── namespace.yaml          # Firebase 프로젝트 네임스페이스
            └── project_count.yaml      # 프로젝트 개수 메트릭
```