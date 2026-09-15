from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.question import (
    Question, KnowledgePoint, QuestionCategory, CategoryType
)
from app.schemas.question_schema import (
    QuestionDetailResponse, QuestionListResponse, KnowledgePointResponse
)

router = APIRouter()

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """获取所有题目分类"""
    categories = db.query(QuestionCategory).all()
    return {"categories": categories}

@router.get("/knowledge-points/{category_id}")
async def get_knowledge_points(
    category_id: int,
    db: Session = Depends(get_db)
) -> List[KnowledgePointResponse]:
    """获取某个分类下的所有知识点"""
    knowledge_points = db.query(KnowledgePoint).filter(
        KnowledgePoint.category_id == category_id
    ).order_by(KnowledgePoint.order).all()
    
    if not knowledge_points:
        raise HTTPException(status_code=404, detail="No knowledge points found")
    
    return knowledge_points

@router.get("/{question_id}", response_model=QuestionDetailResponse)
async def get_question_detail(
    question_id: int,
    db: Session = Depends(get_db)
):
    """获取题目详情"""
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return question

@router.get("/knowledge-point/{knowledge_point_id}")
async def get_questions_by_knowledge_point(
    knowledge_point_id: int,
    db: Session = Depends(get_db)
) -> List[QuestionListResponse]:
    """获取某个知识点下的所有题目"""
    questions = db.query(Question).filter(
        Question.knowledge_point_id == knowledge_point_id
    ).all()
    
    return questions
