from sqlalchemy import Column, Integer, Float, Date, Time
from database import Base

class WorkLog(Base):
    __tablename__ = "work_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    overtime_hours = Column(Float)
    
    # 새로운 필드 추가
    start_time = Column(Time, nullable=True)  # 출근 시간
    end_time = Column(Time, nullable=True)    # 퇴근 시간