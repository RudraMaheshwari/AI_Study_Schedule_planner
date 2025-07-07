TIME_ALLOCATION_PROMPT = """
You are a time management expert for study planning.

Given:
- Total days available: {time_available}
- Daily study hours: {daily_study_time}
- Topic analysis: {topic_analysis}

Calculate optimal time allocation:
1. Total study hours available
2. Hours per topic based on difficulty
3. Reserve 20% time for review and buffer
4. Ensure harder topics get proportionally more time

Provide detailed time breakdown with rationale.
"""