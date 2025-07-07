import streamlit as st

def display_input_form():
    st.header("\U0001F4DD Study Plan Inputs")

    with st.form("study_plan_form"):
        study_goal = st.text_input(
            "\U0001F3AF Study Goal",
            placeholder="e.g., Math Final Exam",
            help="What exam or subject are you preparing for?"
        )

        time_available = st.text_input(
            "\U0001F4C5 Time Available (days)",
            placeholder="e.g., 10",
            help="How many days do you have until your exam?"
        )

        daily_study_time = st.text_input(
            "\u23F0 Daily Study Time (hours)",
            placeholder="e.g., 3",
            help="How many hours can you study each day?"
        )

        topics_to_cover = st.text_area(
            "\U0001F4D6 Topics to Cover",
            placeholder="e.g., Algebra, Geometry, Statistics",
            help="List topics separated by commas"
        )

        submitted = st.form_submit_button(
            "\U0001F680 Generate Study Schedule",
            type="primary",
            use_container_width=True
        )

    return submitted, study_goal, time_available, daily_study_time, topics_to_cover
