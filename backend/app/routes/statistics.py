from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.practice import PracticeSession, PracticeRecord, PracticeStatistics, SessionStatus
from app.schemas.practice_schema import PracticeStatisticsResponse
from app.services.statistics_service import StatisticsService

router = APIRouter()

@router.get("/user/{user_id}")
async def get_user_statistics(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户的学习统计"""
    service = StatisticsService(db)
    return service.get_user_statistics(user_id)

@router.get("/user/{user_id}/knowledge-point/{knowledge_point_id}")
async def get_knowledge_point_statistics(
    user_id: int,
    knowledge_point_id: int,
    db: Session = Depends(get_db)
) -> PracticeStatisticsResponse:
    """获取用户在某个知识点的统计"""
    service = StatisticsService(db)
    return service.get_knowledge_point_statistics(user_id, knowledge_point_id)

@router.get("/user/{user_id}/progress")
async def get_learning_progress(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户的学习进度"""
    service = StatisticsService(db)
    return service.get_learning_progress(user_id)

@router.get("/user/{user_id}/heatmap")
async def get_mastery_heatmap(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户的知识点掌握热力图"""
    service = StatisticsService(db)
    return service.get_mastery_heatmap(user_id)
