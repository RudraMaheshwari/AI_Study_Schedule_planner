import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

def parse_topics(topics_string: str) -> List[str]:
    """Parse comma-separated topics string into list."""
    return [topic.strip() for topic in topics_string.split(',') if topic.strip()]

def calculate_study_dates(start_date: datetime, days: int) -> List[str]:
    """Generate list of study dates."""
    dates = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        dates.append(date.strftime("%Y-%m-%d (%A)"))
    return dates

def distribute_hours(total_hours: float, topic_difficulties: Dict[str, str]) -> Dict[str, float]:
    """Distribute study hours based on topic difficulty."""
    difficulty_weights = {"easy": 1, "medium": 1.5, "hard": 2}
    
    total_weight = sum(difficulty_weights[diff] for diff in topic_difficulties.values())
    
    available_hours = total_hours * 0.8
    
    distribution = {}
    for topic, difficulty in topic_difficulties.items():
        weight = difficulty_weights[difficulty]
        hours = (weight / total_weight) * available_hours
        distribution[topic] = round(hours, 1)
    
    distribution["Review & Practice"] = round(total_hours * 0.2, 1)
    
    return distribution

def create_time_blocks(daily_hours: int) -> List[Dict[str, str]]:
    """Create time blocks for daily study."""
    blocks = []
    start_hour = 9 
    
    session_duration = 1.5 
    break_duration = 0.5    
    
    current_time = start_hour
    remaining_hours = daily_hours
    
    while remaining_hours > 0:
        session_hours = min(session_duration, remaining_hours)
        end_time = current_time + session_hours
        
        blocks.append({
            "start_time": f"{int(current_time):02d}:{int((current_time % 1) * 60):02d}",
            "end_time": f"{int(end_time):02d}:{int((end_time % 1) * 60):02d}",
            "duration": f"{session_hours} hours"
        })
        
        remaining_hours -= session_hours
        current_time = end_time + break_duration
    
    return blocks

def assign_study_methods(topic: str, difficulty: str) -> str:
    """Assign appropriate study methods based on topic and difficulty."""
    methods = {
        "easy": "Reading + Light Practice",
        "medium": "Concept Review + Problem Solving",
        "hard": "Deep Study + Intensive Practice + Examples"
    }
    return methods.get(difficulty, "Reading + Practice")
