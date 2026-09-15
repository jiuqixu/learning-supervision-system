from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"
    CODE = "code"

class QuestionOptionResponse(BaseModel):
    id: int
    option_letter: str
    option_content: str
    explanation: Optional[str] = None
    
    class Config:
        from_attributes = True

class QuestionAnswerResponse(BaseModel):
    id: int
    correct_answer: str
    answer_explanation: Optional[str] = None
    related_knowledge: Optional[dict] = None
    
    class Config:
        from_attributes = True

class QuestionDetailResponse(BaseModel):
    id: int
    title: str
    question_type: str
    difficulty: str
    time_limit: int
    points: int
    description: Optional[str] = None
    options: List[QuestionOptionResponse] = []
    answer: Optional[QuestionAnswerResponse] = None
    
    class Config:
        from_attributes = True

class QuestionListResponse(BaseModel):
    id: int
    title: str
    question_type: str
    difficulty: str
    points: int
    
    class Config:
        from_attributes = True

class KnowledgePointResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    level: str
    
    class Config:
        from_attributes = True
