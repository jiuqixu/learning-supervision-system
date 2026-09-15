from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.practice import (
    PracticeSession, PracticeRecord, WrongQuestionCollection, SessionStatus, SessionType
)
from app.models.question import Question
from app.schemas.practice_schema import (
    PracticeSessionRequest, PracticeSessionResponse, PracticeRecordRequest,
    PracticeRecordResponse, SessionSummary
)
from app.services.practice_service import PracticeService
from app.services.grading_service import GradingService

router = APIRouter()

@router.post("/session/start")
async def start_practice_session(
    request: PracticeSessionRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """开始练习会话"""
    service = PracticeService(db)
    session = service.create_practice_session(
        user_id=user_id,
        session_type=request.session_type,
        knowledge_point_id=request.knowledge_point_id,
        num_questions=request.num_questions
    )
    
    questions = service.get_session_questions(session.id)
    
    return {
        "session_id": session.id,
        "total_questions": session.total_questions,
        "questions": questions
    }

@router.post("/record/submit")
async def submit_answer(
    request: PracticeRecordRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """提交答案并评分"""
    service = PracticeService(db)
    grading_service = GradingService(db)
    
    # 保存答案
    record = service.save_practice_record(
        session_id=request.session_id,
        user_id=user_id,
        question_id=request.question_id,
        user_answer=request.user_answer,
        time_spent=request.time_spent
    )
    
    # 自动评分
    is_correct, points = grading_service.grade_answer(
        question_id=request.question_id,
        user_answer=request.user_answer
    )
    
    # 更新记录
    record.is_correct = is_correct
    record.points_earned = points
    db.commit()
    
    # 如果答错，添加到错题集
    if not is_correct:
        service.add_to_wrong_collection(user_id, request.question_id)
    
    return {
        "record_id": record.id,
        "is_correct": is_correct,
        "points_earned": points,
        "explanation": grading_service.get_answer_explanation(request.question_id)
    }

@router.get("/session/{session_id}")
async def get_session_details(
    session_id: int,
    db: Session = Depends(get_db)
):
    """获取练习会话详情"""
    service = PracticeService(db)
    session = service.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session": session,
        "records": service.get_session_records(session_id),
        "summary": service.get_session_summary(session_id)
    }

@router.post("/session/{session_id}/complete")
async def complete_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """完成练习会话"""
    service = PracticeService(db)
    summary = service.complete_session(session_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return summary

@router.get("/wrong-questions/{user_id}")
async def get_wrong_questions(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户的错题集"""
    wrong_questions = db.query(WrongQuestionCollection).filter(
        WrongQuestionCollection.user_id == user_id,
        WrongQuestionCollection.status == "wrong"
    ).all()
    
    return {"wrong_questions": wrong_questions}
