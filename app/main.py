from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta, date
from database import SessionLocal, engine
from models import Base, WorkLog

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request, year: int = None, month: int = None):
    db = SessionLocal()
    
    query = db.query(WorkLog)
    if year and month:
        from_date = date(year, month, 1)
        to_date = date(year if month < 12 else year + 1, month + 1 if month < 12 else 1, 1)
        query = query.filter(WorkLog.date >= from_date, WorkLog.date < to_date)
    logs = query.order_by(WorkLog.date.desc()).all()
    
    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "logs": logs,
        "selected_year": year,
        "selected_month": month,
        "now": datetime.now()
    })

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

        date_str = date_str.strip()
        work_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        start = datetime.combine(work_date, datetime.min.time()) + timedelta(hours=start_hour, minutes=start_minute)
        end = datetime.combine(work_date, datetime.min.time()) + timedelta(hours=end_hour, minutes=end_minute)
        work_duration = (end - start).total_seconds() / 3600
        overtime = max(0, work_duration - 9)

        entry = db.query(WorkLog).filter(WorkLog.date == work_date).first()

        if entry:
            entry.start_time = start.time()
            entry.end_time = end.time()
            entry.overtime_hours = overtime
        else:
            entry = WorkLog(
                date=work_date,
                overtime_hours=overtime,
                start_time=start.time(),
                end_time=end.time()
            )
            db.add(entry)

        db.commit()

        # ⬇️ db 닫기 전에 로그 리스트 미리 가져오기
        logs = db.query(WorkLog).order_by(WorkLog.date.desc()).limit(10).all()
        db.close()

        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": f"{work_date} 기록 완료!",
            "logs": logs,
            "now": datetime.now(),
        })

    except Exception as e:
        db.rollback()
        db.close()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": f"에러: {str(e)}",
            "logs": []
        })

@app.get("/summary/", response_class=HTMLResponse)
def get_monthly_summary(request: Request, year: int = 2025, month: int = 3):
    db = SessionLocal()
    start_date = date(year, month, 1)
    end_date = date(year if month < 12 else year + 1, month + 1 if month < 12 else 1, 1)

    logs = db.query(WorkLog).filter(WorkLog.date >= start_date, WorkLog.date < end_date).all()

    total_overtime_hours = sum(log.overtime_hours for log in logs)
    total_overtime_minutes = total_overtime_hours * 60
    overtime_hours = int(total_overtime_minutes // 60)
    overtime_minutes = int(total_overtime_minutes % 60)

    all_logs = db.query(WorkLog).order_by(WorkLog.date.desc()).all()

    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_overtime_hours": total_overtime_hours,
        "overtime_hours": overtime_hours,
        "overtime_minutes": overtime_minutes,
        "logs": all_logs,
        "message": f"{year}년 {month}월 총 초과근무: {overtime_hours}시간 {overtime_minutes}분",
        "selected_year": year,
        "selected_month": month,
        "now": datetime.now()
    })
    
@app.get("/logs", response_class=HTMLResponse)
def view_logs(request: Request, year: int = None, month: int = None):
    db = SessionLocal()

    query = db.query(WorkLog)
    if year and month:
        from_date = date(year, month, 1)
        to_date = date(year if month < 12 else year + 1, month + 1 if month < 12 else 1, 1)
        query = query.filter(WorkLog.date >= from_date, WorkLog.date < to_date)

    logs = query.order_by(WorkLog.date.desc()).all()
    db.close()

    return templates.TemplateResponse("logs.html", {
        "request": request,
        "logs": logs,
        "selected_year": year,
        "selected_month": month
    })
    
@app.get("/edit/{log_date}", response_class=HTMLResponse)
def edit_log(request: Request, log_date: str):
    db = SessionLocal()
    entry = db.query(WorkLog).filter(WorkLog.date == log_date).first()
    db.close()

    return templates.TemplateResponse("edit.html", {
        "request": request,
        "entry": entry
    })

@app.post("/edit/{log_date}", response_class=HTMLResponse)
def update_log(
    request: Request,
    log_date: str,
    start_hour: int = Form(...),
    start_minute: int = Form(...),
    end_hour: int = Form(...),
    end_minute: int = Form(...)
):
    db = SessionLocal()
    entry = db.query(WorkLog).filter(WorkLog.date == log_date).first()

    if entry:
        work_date = entry.date
        start = datetime.combine(work_date, datetime.min.time()) + timedelta(hours=start_hour, minutes=start_minute)
        end = datetime.combine(work_date, datetime.min.time()) + timedelta(hours=end_hour, minutes=end_minute)
        work_duration = (end - start).total_seconds() / 3600
        overtime = max(0, work_duration - 9)

        entry.start_time = start.time()
        entry.end_time = end.time()
        entry.overtime_hours = overtime
        db.commit()

    db.close()

    return RedirectResponse(url="/", status_code=302)