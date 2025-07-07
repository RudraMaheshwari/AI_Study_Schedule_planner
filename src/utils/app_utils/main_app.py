import streamlit as st
import os
from dotenv import load_dotenv
from src.agent.study_agent import StudyPlannerAgent
from src.utils.app_utils.components.input_form import display_input_form
from src.utils.app_utils.components.output_display import display_study_plan

load_dotenv()

st.set_page_config(
    page_title="AI Study Schedule Planner",
    page_icon="\U0001F4DA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'agent' not in st.session_state:
    st.session_state.agent = StudyPlannerAgent(
        model_id=os.getenv("AWS_BEDROCK_MODEL_ID"),
        region=os.getenv("AWS_DEFAULT_REGION")
    )

if 'last_generated_plan' not in st.session_state:
    st.session_state.last_generated_plan = None

def main():
    st.title("\U0001F4DA AI Study Schedule Planner")
    st.markdown("**Create a personalized study schedule using AI-powered planning**")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        submitted, study_goal, time_available, daily_study_time, topics_to_cover = display_input_form()

    with col2:
        display_study_plan(submitted, study_goal, time_available, daily_study_time, topics_to_cover)

    st.markdown("---")
