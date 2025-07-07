import os
from dotenv import load_dotenv
from langchain_aws.chat_models import ChatBedrock

load_dotenv()

def get_llm():
    return ChatBedrock(
        region_name=os.getenv("AWS_REGION"),
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_kwargs={
            "temperature": 0.3,
        }
    )
