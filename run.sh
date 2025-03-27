#!/bin/bash

# 가상 환경 경로 설정 (필요한 경우 변경하세요)
VENV_DIR="timetracker"

# 가상 환경이 없다면 생성
if [ ! -d "$VENV_DIR" ]; then
    echo "가상 환경을 생성합니다..."
    python3 -m venv $VENV_DIR
    echo "가상 환경이 생성되었습니다."
fi

# 가상 환경 활성화
echo "가상 환경을 활성화합니다..."
source $VENV_DIR/bin/activate

# 필요한 패키지 설치 (requirements.txt가 있다면)
echo "필요한 패키지를 설치합니다..."
pip install -r requirements.txt

# FastAPI 애플리케이션을 백그라운드에서 실행
echo "FastAPI 애플리케이션을 백그라운드에서 실행합니다..."
nohup uvicorn main:app --reload --port 8888 > app.log 2>&1 &

# 프로세스 ID 확인
echo "FastAPI 애플리케이션이 백그라운드에서 실행 중입니다. 프로세스 ID: $!"