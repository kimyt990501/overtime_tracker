# ⏱️ Overtime Tracker

**Overtime Tracker**는 일일 출근/퇴근 시간을 기록하고,  
9시간 기준 초과근무 시간을 자동 계산하여 월별 총합을 시각화하는 시스템입니다.

- 프론트엔드 & 백엔드는 모두 **FastAPI**
- 데이터베이스는 **MySQL**
- 배포는 **Docker + Kubernetes (Minikube)** 기반

---

## 🏗️ 기술 스택

| 구성 요소       | 기술                     |
|----------------|--------------------------|
| 백엔드/프론트   | FastAPI (Python 3.8)     |
| 데이터베이스    | MySQL 8                  |
| 컨테이너화      | Docker                   |
| 오케스트레이션 | Kubernetes (Minikube)    |
| 자동화 스크립트 | Shell Script + DockerHub |

---

## 📦 주요 기능

- ✅ 출근/퇴근 시간 기록 API
- ✅ 하루 기준 9시간 초과 여부 자동 계산
- ✅ 월별 누적 초과근무 시간 집계
- ✅ 월별 보고서 출력
- ✅ Swagger 문서 자동 생성 (`/docs`)

---

## 🚀 로컬 개발 환경 (Minikube + Kubernetes)

### 🔧 요구사항

- Docker (WSL2 환경 포함)
- Minikube
- kubectl
- DockerHub 계정

---

### ▶️ 클러스터 및 앱 자동 실행

```bash
chmod +x start_k8s.sh
./start_k8s.sh
```

**스크립트가 수행하는 작업:**

- Minikube 클러스터 시작  
- `overtime-app` 네임스페이스 내 파드 상태 확인  
- FastAPI 서버 `/docs` 응답 대기  
- 웹 & DB 포트포워딩 시작  
  - 웹: [http://localhost:8888](http://localhost:8888)  
  - DB: `localhost:13306`

---

### 🌐 웹앱 접속

- [http://localhost:8888/docs](http://localhost:8888/docs)

---

### 🛢️ MySQL 접속 (예: DataGrip)

| 항목      | 값              |
|-----------|-----------------|
| Host      | `127.0.0.1`     |
| Port      | `13306`         |
| Database  | `overtime_db`   |
| Username  | `user`          |
| Password  | `0000`          |

---

## 🐳 Docker 이미지 관리

### 🔨 이미지 빌드 & 푸시

```bash
VERSION=v1.0.0

docker build -t overtime_tracker-web .
docker tag overtime_tracker-web kimyt990501/overtime-web:$VERSION
docker push kimyt990501/overtime-web:$VERSION
```

---

### 🚀 Kubernetes 배포 업데이트

**`overtime_tracker_k8s.yaml` 내 이미지 태그 수정:**

```yaml
containers:
  - name: web
    image: kimyt990501/overtime-web:v1.0.0
```

**배포 적용:**

```bash
minikube kubectl apply -f overtime_tracker_k8s.yaml
```

**또는 롤링 리스타트 방식:**

```bash
minikube kubectl rollout restart deploy/web -n overtime-app
```

---

## 🗂️ 프로젝트 구조

```text
overtime_tracker/
├── app/
│   ├── main.py                 # FastAPI 진입점
│   ├── models.py               # SQLAlchemy 모델 정의
│   ├── database.py             # DB 세션 및 엔진 구성
│   └── ...                     # 기타 라우터 및 유틸
├── start.sh                    # FastAPI 앱 실행 스크립트
├── Dockerfile                  # 웹앱 Docker 이미지 정의
├── docker-compose.yaml         # 로컬 개발용 Docker 구성
├── overtime_tracker_k8s.yaml   # Kubernetes 리소스 정의
├── start_k8s.sh                # Minikube 자동 실행 스크립트
└── README.md                   # 프로젝트 설명 파일
```

---

## 📈 향후 개선 예정

- [ ] Ingress + HTTPS 적용
- [ ] Grafana + Prometheus 기반 모니터링
- [ ] GitHub Actions 기반 CI/CD 자동화
- [ ] JWT 인증 및 사용자 권한 분리

---

## 👨‍💻 개발자 정보

- **GitHub**: [@kimyt990501](https://github.com/kimyt990501)
- **DockerHub**: [kimyt990501](https://hub.docker.com/u/kimyt990501)

---

## 📝 라이선스

```
MIT License
```