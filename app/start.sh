#!/bin/bash

echo "DB가 준비될 때까지 기다리는 중..."

# MySQL 연결될 때까지 반복 시도
until mysqladmin ping -h db -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
  echo "아직 DB가 안 됐어요... 2초 뒤 재시도"
  sleep 2
done

echo "DB 연결 성공! FastAPI 시작합니다..."

# FastAPI 앱 실행
exec uvicorn main:app --host 0.0.0.0 --port 8888 --reload