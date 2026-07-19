import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

from agents.config import base_url
from agents.memory.tools import search_facts, search_nodes

from .prompt import taro_prompt


async def create_tarot_agent():
    llm = ChatOpenAI(base_url=base_url, model='openai/gpt-5-mini', temperature=0.2)

    tarot_mcp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../tarotmcp/dist/index.js"))

    client = MultiServerMCPClient(
        {
            "tarot": {
                "command": "node",
                "args": [tarot_mcp_path],
                "transport": "stdio"
            },
        }
    )

    tools = await client.get_tools()
    tools_node = ToolNode(tools + [search_facts, search_nodes])
    agent = llm.bind_tools(tools + [search_facts, search_nodes])
    tarot_agent_chain = taro_prompt | agent

    return tarot_agent_chain, tools_node
