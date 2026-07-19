import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

from agents.config import base_url

from .prompt import astro_prompt


async def create_astro_agent():
    # Memory tools land in Plan 03 (agents.memory.tools); lazy import keeps this package importable now.
    from agents.memory.tools import search_facts, search_nodes

    llm = ChatOpenAI(model='openai/gpt-5-mini', base_url=base_url, temperature=0.7)

    astro_mcp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../astromcp/dist/main.js"))

    client = MultiServerMCPClient(
        {
            "astrology":
                {
                "command": "node",
                "args": [astro_mcp_path],
                "transport": "stdio"
                }
         }
    )

    tools = await client.get_tools()
    tools_node = ToolNode(tools + [search_facts, search_nodes])
    agent = llm.bind_tools(tools + [search_facts, search_nodes])

    astro_agent_chain = astro_prompt | agent

    return astro_agent_chain, tools_node
