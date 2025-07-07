OPTIMIZATION_PROMPT = """
Optimize the study plan for maximum effectiveness.

Current plan: {daily_schedule}
Time allocation: {time_allocation}

Apply these optimization principles:
1. Place harder topics earlier when energy is high
2. Alternate between different types of content
3. Include spaced repetition
4. Add buffer time for catch-up
5. Schedule intensive review before exam

Provide the final optimized plan with clear rationale.
"""