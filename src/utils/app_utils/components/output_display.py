import streamlit as st
from src.utils.helpers import validate_inputs, format_study_plan, save_plan_to_session
from src.utils.generate_pdf_helper import generate_pdf_from_text

def display_study_plan(submitted, study_goal, time_available, daily_study_time, topics_to_cover):
    st.header("\U0001F4CB Generated Study Plan")

    if submitted:
        is_valid, error_message = validate_inputs(
            study_goal, time_available, daily_study_time, topics_to_cover
        )

        if not is_valid:
            st.error(f"\u274C {error_message}")
        else:
            with st.spinner("\U0001F504 Creating your personalized study plan..."):
                try:
                    plan = st.session_state.agent.create_study_plan(
                        study_goal=study_goal,
                        time_available=int(time_available),
                        daily_study_time=int(daily_study_time),
                        topics_string=topics_to_cover
                    )

                    save_plan_to_session(plan, st.session_state)

                    st.success("\u2705 Study plan generated successfully!")

                    formatted_plan = format_study_plan(plan)
                    st.markdown(formatted_plan)

                    pdf_buffer = generate_pdf_from_text(formatted_plan)

                    st.download_button(
                        label="\U0001F4E5 Download Study Plan",
                        data=pdf_buffer,
                        file_name=f"study_plan_{study_goal.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )

                except Exception as e:
                    st.error(f"\u274C Error generating plan: {str(e)}")
    elif st.session_state.last_generated_plan:
        st.info("\U0001F4C4 Showing last generated plan")
        formatted_plan = format_study_plan(st.session_state.last_generated_plan)
        st.markdown(formatted_plan)
