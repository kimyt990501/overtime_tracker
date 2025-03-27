FROM python:3.8-slim

# mysqladmin 설치를 위한 기본 패키지 추가
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

COPY ./app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/start.sh

EXPOSE 8888

CMD ["/app/start.sh"]