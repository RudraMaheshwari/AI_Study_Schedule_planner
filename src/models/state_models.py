from typing import TypedDict, List, Dict, Optional
from pydantic import BaseModel

class StudyPlanState(TypedDict):
    study_goal: str
    time_available: int
    daily_study_time: int
    topics_to_cover: List[str]
    goal_analysis: Optional[Dict]
    time_allocation: Optional[Dict]
    daily_schedule: Optional[Dict]
    final_plan: Optional[Dict]
    planning_summary: Optional[str]

class TopicAnalysis(BaseModel):
    topic: str
    difficulty: str
    priority: int
    estimated_hours: float

class DailySchedule(BaseModel):
    day: int
    date: str
    topics: List[str]
    time_blocks: List[Dict[str, str]]
    study_method: str
    break_time: str

class StudyPlan(BaseModel):
    daily_schedules: List[DailySchedule]
    topic_allocations: Dict[str, float]
    total_study_hours: float
    review_days: List[int]
    strategy_explanation: str
    planning_rationale: str