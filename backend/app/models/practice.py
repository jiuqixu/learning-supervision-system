from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class SessionType(str, enum.Enum):
    KNOWLEDGE_POINT = "knowledge_point"
    MOCK_EXAM = "mock_exam"
    WRONG_QUESTIONS = "wrong_questions"
    RANDOM = "random"

class SessionStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"

class MasteryLevel(str, enum.Enum):
    UNKNOWN = "unknown"
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"

class PracticeSession(Base):
    __tablename__ = "practice_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    session_name = Column(String(255))
    session_type = Column(Enum(SessionType), nullable=False)
    knowledge_point_id = Column(Integer)
    total_questions = Column(Integer)
    status = Column(Enum(SessionStatus), default=SessionStatus.IN_PROGRESS)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    time_spent = Column(Integer)  # 秒
    score = Column(Integer)
    
    records = relationship("PracticeRecord", back_populates="session", cascade="all, delete-orphan")

class PracticeRecord(Base):
    __tablename__ = "practice_records"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("practice_sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    order_in_session = Column(Integer)
    user_answer = Column(Text)
    is_correct = Column(Boolean)
    points_earned = Column(Integer)
    time_spent = Column(Integer)  # 秒
    answered_at = Column(DateTime, default=datetime.utcnow)
    marked_for_review = Column(Boolean, default=False)
    teacher_feedback = Column(Text)
    
    session = relationship("PracticeSession", back_populates="records")
    question = relationship("Question", back_populates="practice_records")

class WrongQuestionCollection(Base):
    __tablename__ = "wrong_question_collection"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    first_wrong_at = Column(DateTime, default=datetime.utcnow)
    wrong_count = Column(Integer, default=1)
    last_wrong_at = Column(DateTime)
    status = Column(String(50), default="wrong")  # wrong, mastered, reviewing
    personal_note = Column(Text)
    
    question = relationship("Question", back_populates="wrong_collections")

class PracticeStatistics(Base):
    __tablename__ = "practice_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    knowledge_point_id = Column(Integer)
    total_practiced = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    accuracy_rate = Column(Float, default=0.0)
    last_practiced_at = Column(DateTime)
    average_time_spent = Column(Integer, default=0)  # 秒
    mastery_level = Column(Enum(MasteryLevel), default=MasteryLevel.UNKNOWN)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
