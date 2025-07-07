DAILY_SCHEDULE_PROMPT = """
Create a detailed daily study schedule.

Input:
- Days available: {time_available}
- Daily hours: {daily_study_time}
- Time allocation: {time_allocation}
- Topics: {topics_to_cover}

Create a day-by-day schedule including:
1. Specific topics for each day
2. Time blocks with start/end times
3. Study methods (reading, practice, review)
4. Break times
5. Review sessions in final days

Make it realistic and achievable.
"""