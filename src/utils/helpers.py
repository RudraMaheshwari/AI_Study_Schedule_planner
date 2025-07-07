import json
from datetime import datetime
from typing import Dict, Any

def format_study_plan(plan_data: Dict[str, Any]) -> str:
    """Format the study plan for display."""
    output = []
    
    output.append("# \U0001F4DA Personalized Study Schedule")
    output.append("=" * 50)
    output.append("")
    
    if "planning_summary" in plan_data:
        output.append("## \U0001F4CB Planning Summary")
        output.append(plan_data["planning_summary"])
        output.append("")
    
    if "time_allocation" in plan_data:
        output.append("## \u23F0 Time Allocation per Topic")
        for topic, hours in plan_data["time_allocation"].items():
            output.append(f"• **{topic}**: {hours} hours")
        output.append("")
    
    if "daily_schedule" in plan_data:
        output.append("## \U0001F4C5 Daily Study Schedule")
        for day_info in plan_data["daily_schedule"]:
            output.append(f"### Day {day_info['day']}: {day_info['date']}")
            output.append(f"**Topics**: {', '.join(day_info['topics'])}")
            output.append(f"**Study Method**: {day_info['study_method']}")
            
            output.append("**Time Blocks**:")
            for block in day_info['time_blocks']:
                output.append(f"  - {block['start_time']} - {block['end_time']} ({block['duration']})")
            
            output.append(f"**Break Time**: {day_info['break_time']}")
            output.append("")
    
    return "\n".join(output)

def validate_inputs(study_goal: str, time_available: str, daily_study_time: str, topics: str) -> tuple[bool, str]:
    """Validate user inputs."""
    try:
        if not study_goal.strip():
            return False, "Study goal cannot be empty"
        
        days = int(time_available)
        if days < 1 or days > 60:
            return False, "Time available must be between 1 and 30 days"
        
        hours = float(daily_study_time)
        if hours < 0.5 or hours > 12:
            return False, "Daily study time must be between 0.5 and 12 hours"
        
        topic_list = [t.strip() for t in topics.split(',') if t.strip()]
        if len(topic_list) < 2 or len(topic_list) > 60:
            return False, "Please provide between 2 and 20 topics"
        
        return True, "Valid inputs"
    
    except ValueError:
        return False, "Please enter valid numbers for time and hours"

def save_plan_to_session(plan: Dict[str, Any], session_state) -> None:
    """Save the generated plan to session state."""
    session_state.last_generated_plan = plan
    session_state.plan_generation_time = datetime.now()