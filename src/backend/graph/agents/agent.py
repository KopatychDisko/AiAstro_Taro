from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import ToolNode
from zep_cloud.client import AsyncZep

from .config import base_url, zep_api

from .prompt import *
from .schemas import RouterOutput, ImgOutput, Agents, UnlockCard, Summarize

import os

zep = AsyncZep(api_key=zep_api)

@tool
async def search_facts(config: RunnableConfig, query: str, limit: int = 3) -> list[str]:
    """Search for facts in all conversations had with a user.
    
    Args:
        query (str): The search query.
        limit (int): The number of results to return. Defaults to 3.
    Returns:
        list: A list of facts that match the search query.
    """
    edges = await zep.graph.search(
        user_id=config['configurable']["thread_id"], text=query, limit=limit, search_scope="edges"
    )
    return [edge.fact for edge in edges]

@tool
async def search_nodes(config: RunnableConfig, query: str, limit: int = 3) -> list[str]:
    """Search for nodes in all conversations had with a user.
    
    Args:
        query (str): The search query.
        limit (int): The number of results to return. Defaults to 3.
    Returns:
        list: A list of node summaries for nodes that match the search query.
    """
    nodes = await zep.graph.search(
        user_id=config['configurable']["thread_id"], text=query, limit=limit, search_scope="nodes"
    )
    return [node.summary for node in nodes]


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


async def create_astro_agent():
    llm = ChatOpenAI(model='openai/gpt-5-mini',base_url=base_url, temperature=0.7)
    
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

def create_router_agent():
    llm = ChatOpenAI(model='openai/gpt-5-nano',base_url=base_url, temperature=0)
    
    agent = router_prompt | llm.with_structured_output(RouterOutput)
    
    return agent

def create_img_agent():
    llm = ChatOpenAI(model='openai/gpt-5-mini',base_url=base_url, temperature=0)
    
    agent = img_prompt | llm.with_structured_output(ImgOutput)
    return agent

def create_card_unlock_agent():
    llm = ChatOpenAI(model='qwen/qwq-32b', base_url=base_url, temperature=0)
    agent = unlock_card_prompt | llm.with_structured_output(UnlockCard)
    
    return agent

def create_summarize_agent():
    llm = ChatOpenAI(model='deepseek/deepseek-chat-v3.1', base_url=base_url, temperature=0)
    agent = summarize_prompt | llm.with_structured_output(Summarize)
    
    return agent

async def create_agents():
    taro_agent, taro_tool = await create_tarot_agent()
    astro_agent, astro_tool = await create_astro_agent()
    router_agent = create_router_agent()
    img_agent = create_img_agent()
    unlock_card_agent = create_card_unlock_agent()
    summarize_agent = create_summarize_agent()
    return Agents(
        taro_agent=taro_agent, 
        taro_tool=taro_tool, 
        astro_agent=astro_agent, 
        astro_tool=astro_tool,
        router_agent=router_agent, 
        img_agent=img_agent,
        unlock_card_agent=unlock_card_agent,
        summarize_agent=summarize_agent
        )