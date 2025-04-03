FROM python:3.8-slim

# mysqladmin + curl 설치를 위한 기본 패키지 추가
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 앱 복사 및 작업 디렉토리 설정
COPY ./app /app
WORKDIR /app

# 파이썬 패키지 설치 및 실행 권한 부여
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/start.sh

# FastAPI 포트
EXPOSE 8888

# 실행 스크립트
CMD ["/app/start.sh"]