from langchain_openai import ChatOpenAI

from agents.config import base_url
from agents.state import RouterOutput

from .prompt import router_prompt


def create_router_agent():
    llm = ChatOpenAI(model='openai/gpt-5-nano', base_url=base_url, temperature=0)

    agent = router_prompt | llm.with_structured_output(RouterOutput).with_retry(stop_after_attempt=2)

    return agent
