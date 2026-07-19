import logging
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

from agents.config import base_url
from agents.memory.tools import search_facts, search_nodes

from .prompt import astro_prompt

logger = logging.getLogger(__name__)


async def create_astro_agent():
    llm = ChatOpenAI(model='openai/gpt-5-mini', base_url=base_url, temperature=0.7)

    astro_mcp_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../astromcp/dist/main.js")
    )
    mcp_tools = []

    if os.path.isfile(astro_mcp_path):
        client = MultiServerMCPClient(
            {
                "astrology": {
                    "command": "node",
                    "args": [astro_mcp_path],
                    "transport": "stdio",
                }
            }
        )
        mcp_tools = await client.get_tools()
    else:
        logger.warning(
            "Astro MCP not built (%s) — starting without astrology tools (deferred v2)",
            astro_mcp_path,
        )

    tools = mcp_tools + [search_facts, search_nodes]
    tools_node = ToolNode(tools)
    agent = llm.bind_tools(tools)
    astro_agent_chain = astro_prompt | agent

    return astro_agent_chain, tools_node
