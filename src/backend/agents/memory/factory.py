from langchain_openai import ChatOpenAI

from agents.config import base_url
from agents.state import Summarize

from .prompt import summarize_prompt


def create_summarize_agent():
    llm = ChatOpenAI(model='deepseek/deepseek-chat-v3.1', base_url=base_url, temperature=0)
    agent = summarize_prompt | llm.with_structured_output(Summarize).with_retry(stop_after_attempt=2)

    return agent
