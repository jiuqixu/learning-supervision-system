from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SessionType(str, Enum):
    KNOWLEDGE_POINT = "knowledge_point"
    MOCK_EXAM = "mock_exam"
    WRONG_QUESTIONS = "wrong_questions"
    RANDOM = "random"

class PracticeRecordRequest(BaseModel):
    session_id: int
    question_id: int
    user_answer: str
    time_spent: int
    marked_for_review: Optional[bool] = False

class PracticeRecordResponse(BaseModel):
    id: int
    question_id: int
    user_answer: str
    is_correct: Optional[bool] = None
    points_earned: Optional[int] = None
    time_spent: int
    answered_at: datetime
    
    class Config:
        from_attributes = True

class PracticeSessionRequest(BaseModel):
    session_type: str
    knowledge_point_id: Optional[int] = None
    num_questions: int = 10

class PracticeSessionResponse(BaseModel):
    id: int
    session_type: str
    total_questions: int
    status: str
    started_at: datetime
    score: Optional[int] = None
    records: List[PracticeRecordResponse] = []
    
    class Config:
        from_attributes = True

class PracticeStatisticsResponse(BaseModel):
    knowledge_point_id: Optional[int] = None
    total_practiced: int
    correct_count: int
    wrong_count: int
    accuracy_rate: float
    mastery_level: str
    last_practiced_at: Optional[datetime] = None
    average_time_spent: int
    
    class Config:
        from_attributes = True

class SessionSummary(BaseModel):
    session_id: int
    total_questions: int
    correct_count: int
    accuracy: str
    total_points: int
    time_spent: int
    completed_at: datetime
