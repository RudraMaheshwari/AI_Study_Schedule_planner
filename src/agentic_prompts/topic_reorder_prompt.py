TOPIC_REORDER_PROMPT = """
You are a study planning assistant. The user has provided a list of study topics in an unstructured or random order.

Your task is to reorder these topics in a **logical learning sequence**, from foundational concepts to more advanced topics. Assume the learner is starting from basic or no knowledge and wants to build up understanding gradually.

### Input Topics
{topics_string}

### Instructions
- Reorder the topics logically, ensuring that prerequisites come before advanced topics.
- Do not remove or add new topics.
- Do not group them by theme—focus on learning sequence.
- This is not specific to any programming language or subject area.

### Output Format
Return a Python-style list of strings in the new order, like:
["Basics", "Intermediate Concept", "Advanced Topic", ...]

Only return the reordered list.
"""
