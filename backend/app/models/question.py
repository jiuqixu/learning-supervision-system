from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"
    CODE = "code"

class CategoryType(str, enum.Enum):
    ENGLISH = "english"
    NETWORK_SECURITY = "network_security"

class QuestionCategory(Base):
    __tablename__ = "question_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    category_type = Column(Enum(CategoryType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    knowledge_points = relationship("KnowledgePoint", back_populates="category")

class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("question_categories.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    level = Column(Enum(DifficultyLevel), default=DifficultyLevel.EASY)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category = relationship("QuestionCategory", back_populates="knowledge_points")
    questions = relationship("Question", back_populates="knowledge_point")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_point_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    points = Column(Integer, default=10)
    time_limit = Column(Integer, default=300)  # 秒
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    knowledge_point = relationship("KnowledgePoint", back_populates="questions")
    content = relationship("QuestionContent", uselist=False, back_populates="question", cascade="all, delete-orphan")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")
    answer = relationship("QuestionAnswer", uselist=False, back_populates="question", cascade="all, delete-orphan")
    practice_records = relationship("PracticeRecord", back_populates="question")
    wrong_collections = relationship("WrongQuestionCollection", back_populates="question")

class QuestionContent(Base):
    __tablename__ = "question_content"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), unique=True, nullable=False)
    content_html = Column(Text)  # 富文本内容
    code_snippet = Column(Text)  # 代码片段
    attachments = Column(JSON)  # 图片和资源链接
    
    question = relationship("Question", back_populates="content")

class QuestionOption(Base):
    __tablename__ = "question_options"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    option_letter = Column(String(1))  # A, B, C, D, E
    option_content = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    explanation = Column(Text)
    
    question = relationship("Question", back_populates="options")

class QuestionAnswer(Base):
    __tablename__ = "question_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), unique=True, nullable=False)
    correct_answer = Column(Text, nullable=False)
    answer_explanation = Column(Text)
    related_knowledge = Column(JSON)  # 相关知识点
    difficulty_reason = Column(Text)  # 难度原因
    
    question = relationship("Question", back_populates="answer")
