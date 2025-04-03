from sqlalchemy import Column, Integer, Float, Date, Time, DateTime
from sqlalchemy.sql import func
from database import Base

class WorkLog(Base):
    __tablename__ = "work_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    overtime_hours = Column(Float)
    start_time = Column(Time, nullable=True)  # 출근 시간
    end_time = Column(Time, nullable=True)    # 퇴근 시간
    overtime_hours = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), default= func.now())