#!/bin/bash

export MINIKUBE_HOME=/home/kimyt990501
export KUBECONFIG=/home/kimyt990501/.kube/config

echo "포트포워딩용 스크립트 실행 중..."

echo "파드 상태:"
minikube kubectl -- get pods -n overtime-app

# web 파드 Ready 될 때까지 대기
echo "web 파드 준비 중..."
until minikube kubectl -- get pod -n overtime-app -l app=web -o jsonpath="{.items[0].status.containerStatuses[0].ready}" 2>/dev/null | grep -q true; do
  echo "  → 아직 준비 안 됨. 2초 대기..."
  sleep 2
done

echo "web 파드 준비 완료!"

echo "🌡 FastAPI 서버 헬스체크 대기 중 (파드 내부 요청)..."
until minikube kubectl -- exec -n overtime-app "$(minikube kubectl -- get pod -l app=web -n overtime-app -o jsonpath="{.items[0].metadata.name}")" -- curl -s http://localhost:8888/docs > /dev/null; do
  echo "  → 아직 FastAPI 서버 준비 안 됨... 10초 대기"
  sleep 10
done

echo "FastAPI 서버 응답 확인됨! 포트포워딩 시작"

echo "웹 포트포워딩 시작 (localhost:8888)..."
nohup minikube kubectl -- port-forward svc/web 8888:8888 -n overtime-app --address 0.0.0.0 > web.log 2>&1 &

sleep 2

echo "MySQL 포트포워딩 시작 (localhost:13306)..."
nohup minikube kubectl -- port-forward svc/mysql 13306:3306 -n overtime-app > mysql.log 2>&1 &

sleep 2

echo "✅ 모든 포트포워딩 완료!"
echo "웹: http://localhost:8888"
echo "DB: 127.0.0.1:13306 (user / 0000)"