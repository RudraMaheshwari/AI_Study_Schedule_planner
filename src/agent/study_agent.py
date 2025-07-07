import json
from datetime import datetime
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from src.models.state_models import StudyPlanState
from src.agentic_prompts.daily_schedule_prompt import DAILY_SCHEDULE_PROMPT
from src.agentic_prompts.goal_analysis_prompt import GOAL_ANALYSIS_PROMPT
from src.agentic_prompts.optimization_prompt import OPTIMIZATION_PROMPT
from src.agentic_prompts.time_allocation_prompt import TIME_ALLOCATION_PROMPT
from src.agentic_prompts.topic_reorder_prompt import TOPIC_REORDER_PROMPT
from src.tools.planning_tools import (
    parse_topics, calculate_study_dates, distribute_hours,
    create_time_blocks, assign_study_methods
)
from src.models.llm_config import get_llm
from langgraph.prebuilt import create_react_agent

class StudyPlannerAgent:
    def __init__(self, model_id: str, region: str):
        self.llm = get_llm()
        self.memory = MemorySaver()
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        workflow = StateGraph(StudyPlanState)
        
        workflow.add_node("reorder_topics", self._reorder_topics)
        workflow.add_node("goal_analysis", self._analyze_goal)
        workflow.add_node("time_allocation", self._allocate_time)
        workflow.add_node("daily_schedule", self._create_daily_schedule)
        workflow.add_node("optimization", self._optimize_plan)

        workflow.set_entry_point("reorder_topics")
        workflow.add_edge("reorder_topics", "goal_analysis")
        workflow.add_edge("goal_analysis", "time_allocation")
        workflow.add_edge("time_allocation", "daily_schedule")
        workflow.add_edge("daily_schedule", "optimization")
        workflow.add_edge("optimization", END)
        
        return workflow.compile(checkpointer=self.memory)

    def _reorder_topics(self, state: StudyPlanState) -> StudyPlanState:
        """Preprocessing Step: Reorder topics using LLM before goal analysis."""
        original_topics = state["topics_to_cover"]
        prompt = TOPIC_REORDER_PROMPT.format(
            topics_string=", ".join(original_topics)
        )
        response = self.llm.invoke([HumanMessage(content=prompt)])

        try:
            reordered_topics = json.loads(response.content)
        except json.JSONDecodeError:
            reordered_topics = original_topics

        state["topics_to_cover"] = reordered_topics
        return state

    def _analyze_goal(self, state: StudyPlanState) -> StudyPlanState:
        """Step 1: Analyze study goal and topics."""
        topics = state["topics_to_cover"]
        prompt = GOAL_ANALYSIS_PROMPT.format(
            study_goal=state["study_goal"],
            topics_to_cover=", ".join(topics)
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])

        goal_analysis = {
            "topics": topics,
            "difficulty_mapping": {}
        }

        for i, topic in enumerate(topics):
            if i == 0:
                difficulty = "medium"
            elif i == 1:
                difficulty = "hard"
            elif i == 2:
                difficulty = "easy"
            else:
                difficulty = "medium"
            goal_analysis["difficulty_mapping"][topic] = difficulty
        
        goal_analysis["analysis_result"] = response.content
        state["goal_analysis"] = goal_analysis
        return state

    def _allocate_time(self, state: StudyPlanState) -> StudyPlanState:
        """Step 2: Allocate time across topics."""
        total_hours = state["time_available"] * state["daily_study_time"]
        difficulty_mapping = state["goal_analysis"]["difficulty_mapping"]
        
        time_allocation = distribute_hours(total_hours, difficulty_mapping)
        
        prompt = TIME_ALLOCATION_PROMPT.format(
            time_available=state["time_available"],
            daily_study_time=state["daily_study_time"],
            topic_analysis=json.dumps(state["goal_analysis"], indent=2)
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        state["time_allocation"] = {
            "total_hours": total_hours,
            "topic_hours": time_allocation,
            "allocation_rationale": response.content
        }
        return state

    def _create_daily_schedule(self, state: StudyPlanState) -> StudyPlanState:
        """Step 3: Create detailed daily schedule."""
        start_date = datetime.now()
        study_dates = calculate_study_dates(start_date, state["time_available"])
        
        daily_schedules = []
        topic_hours = state["time_allocation"]["topic_hours"]
        topics = list(topic_hours.keys())
        
        study_topics = [t for t in topics if t != "Review & Practice"]
        
        current_topic_idx = 0
        for day in range(state["time_available"]):
            if day >= state["time_available"] - 2:
                day_topics = ["Review & Practice"]
                study_method = "Comprehensive Review + Practice Tests"
            else:
                day_topics = [study_topics[current_topic_idx % len(study_topics)]]
                difficulty = state["goal_analysis"]["difficulty_mapping"].get(day_topics[0], "medium")
                study_method = assign_study_methods(day_topics[0], difficulty)
                current_topic_idx += 1
            
            time_blocks = create_time_blocks(state["daily_study_time"])
            
            daily_schedules.append({
                "day": day + 1,
                "date": study_dates[day],
                "topics": day_topics,
                "time_blocks": time_blocks,
                "study_method": study_method,
                "break_time": "15 minutes between sessions"
            })
        
        state["daily_schedule"] = daily_schedules
        return state

    def _optimize_plan(self, state: StudyPlanState) -> StudyPlanState:
        """Step 4: Optimize the study plan."""
        prompt = OPTIMIZATION_PROMPT.format(
            daily_schedule=json.dumps(state["daily_schedule"], indent=2),
            time_allocation=json.dumps(state["time_allocation"], indent=2)
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        final_plan = {
            "daily_schedule": state["daily_schedule"],
            "time_allocation": state["time_allocation"]["topic_hours"],
            "total_study_hours": state["time_allocation"]["total_hours"],
            "optimization_notes": response.content
        }
        
        planning_summary = f"""
            **Study Goal**: {state['study_goal']}
            **Duration**: {state['time_available']} days
            **Daily Commitment**: {state['daily_study_time']} hours
            **Total Study Time**: {state['time_allocation']['total_hours']} hours

            **Strategy**: The plan prioritizes harder topics early when mental energy is highest, 
            includes regular breaks, and reserves the final days for comprehensive review.
        """.strip()
        
        state["final_plan"] = final_plan
        state["planning_summary"] = planning_summary
        return state

    def create_study_plan(self, study_goal: str, time_available: int, 
                        daily_study_time: int, topics_string: str) -> Dict[str, Any]:
        """Main method to create a study plan."""
        topics = parse_topics(topics_string)
        
        initial_state = StudyPlanState(
            study_goal=study_goal,
            time_available=time_available,
            daily_study_time=daily_study_time,
            topics_to_cover=topics,
            goal_analysis=None,
            time_allocation=None,
            daily_schedule=None,
            final_plan=None,
            planning_summary=None
        )
        
        config = {"configurable": {"thread_id": "study_plan_session"}}
        final_state = self.graph.invoke(initial_state, config)
        
        return {
            "daily_schedule": final_state["daily_schedule"],
            "time_allocation": final_state["time_allocation"]["topic_hours"],
            "planning_summary": final_state["planning_summary"],
            "optimization_notes": final_state["final_plan"]["optimization_notes"]
        }
