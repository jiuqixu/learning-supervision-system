from .questions import router as questions_router
from .practice import router as practice_router
from .statistics import router as statistics_router

__all__ = ["questions_router", "practice_router", "statistics_router"]
