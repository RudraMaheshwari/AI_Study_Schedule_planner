GOAL_ANALYSIS_PROMPT = """
You are an expert study planner. Analyze the given study goal and topics.

Study Goal: {study_goal}
Topics to Cover: {topics_to_cover}

Please analyze each topic and provide:
1. Difficulty level (easy/medium/hard) for each topic
2. Priority order (1 = highest priority)
3. Estimated relative complexity

Consider factors like:
- Mathematical complexity
- Conceptual difficulty
- Typical student challenges
- Prerequisites and dependencies

Provide your analysis in a structured format.
"""
