from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta, date
from database import SessionLocal, engine
from models import Base, WorkLog

Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/log", response_class=HTMLResponse)
def log_overtime(
    request: Request,
    date_str: str = Form(...),
    start_hour: int = Form(...),
    start_minute: int = Form(...),
    end_hour: int = Form(...),
    end_minute: int = Form(...),
):
    try:
        db = SessionLocal()

        # 공백 제거 후 날짜 처리
        date_str = date_str.strip()  # 양쪽 공백을 제거
        work_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # 출근 시간과 퇴근 시간 계산
        start = datetime.combine(work_date, datetime.min.time()) + timedelta(hours=start_hour, minutes=start_minute)
        end = datetime.combine(work_date, datetime.min.time()) + timedelta(hours=end_hour, minutes=end_minute)

        # 근무 시간 계산
        work_duration = (end - start).total_seconds() / 3600
        overtime = max(0, work_duration - 9)  # 9시간 초과분 계산

        # 기존 날짜가 있는지 확인
        entry = db.query(WorkLog).filter(WorkLog.date == work_date).first()

        if entry:
            # 기존 데이터가 있으면 업데이트
            entry.start_time = start.time()
            entry.end_time = end.time()
            entry.overtime_hours = overtime
        else:
            # 기존 데이터가 없으면 새로 추가
            entry = WorkLog(
                date=work_date,
                overtime_hours=overtime,
                start_time=start.time(),
                end_time=end.time()
            )
            db.add(entry)

        db.commit()
        db.close()

        return templates.TemplateResponse("index.html", {"request": request, "message": f"{work_date} 기록 완료!"})

    except Exception as e:
        db.rollback()
        db.close()
        return templates.TemplateResponse("index.html", {"request": request, "message": f"에러: {str(e)}"})

@app.get("/summary/", response_class=HTMLResponse)
def get_monthly_summary(request: Request, year: int = 2025, month: int = 3):
    db = SessionLocal()
    start_date = date(year, month, 1)
    end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
    logs = db.query(WorkLog).filter(WorkLog.date >= start_date, WorkLog.date < end_date).all()

    # 총 초과근무 시간 계산 (시간 단위)
    total_overtime_hours = sum(log.overtime_hours for log in logs)

    # 총 초과근무 시간을 시간과 분으로 나누기
    total_overtime_minutes = total_overtime_hours * 60
    overtime_hours = int(total_overtime_minutes // 60)  # 시간 계산
    overtime_minutes = int(total_overtime_minutes % 60)  # 분 계산

    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_overtime_hours": total_overtime_hours,
        "overtime_hours": overtime_hours,
        "overtime_minutes": overtime_minutes,
        "message": f"{year}년 {month}월 총 초과근무: {overtime_hours}시간 {overtime_minutes}분"
    })