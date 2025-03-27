from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# MySQL 접속 URL
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://user:0000@localhost/overtime_db"

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./worklog.db") 

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()