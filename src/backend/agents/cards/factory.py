from langchain_openai import ChatOpenAI

from agents.config import base_url
from agents.state import UnlockCard

from .prompt import unlock_card_prompt


def create_card_unlock_agent():
    llm = ChatOpenAI(model='qwen/qwq-32b', base_url=base_url, temperature=0)
    agent = unlock_card_prompt | llm.with_structured_output(UnlockCard).with_retry(stop_after_attempt=2)

    return agent
