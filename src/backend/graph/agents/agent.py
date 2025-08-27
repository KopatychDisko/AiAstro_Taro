from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import ToolNode

from .config import base_url

from .prompt import taro_prompt, astro_prompt, router_prompt, img_prompt, unlock_card_prompt
from .schemas import RouterOutput, ImgOutput, Agents, UnlockCard

import os

async def create_tarot_agent():
    llm = ChatOpenAI(base_url=base_url, model='openai/gpt-5-nano', temperature=0.2)
    
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
    tools_node = ToolNode(tools)
    agent = llm.bind_tools(tools)
    tarot_agent_chain = taro_prompt | agent
    
    return tarot_agent_chain, tools_node


async def create_astro_agent():
    llm = ChatOpenAI(model='openai/gpt-4.1-nano',base_url=base_url, temperature=0.7)
    
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
    tools_node = ToolNode(tools)
    agent = llm.bind_tools(tools)
    
    astro_agent_chain = astro_prompt | agent
    
    return astro_agent_chain, tools_node

def create_router_agent():
    llm = ChatOpenAI(model='openai/gpt-5-nano',base_url=base_url, temperature=0)
    
    agent = router_prompt | llm.with_structured_output(RouterOutput)
    
    return agent

def create_img_agent():
    llm = ChatOpenAI(model='openai/gpt-4o-mini-2024-07-18',base_url=base_url, temperature=0)
    
    agent = img_prompt | llm.with_structured_output(ImgOutput)
    return agent

def create_card_unlock_agent():
    llm = ChatOpenAI(model='qwen/qwq-32b', base_url=base_url, temperature=0)
    agent = unlock_card_prompt | llm.with_structured_output(UnlockCard)
    
    return agent

async def create_agents():
    taro_agent, taro_tool = await create_tarot_agent()
    astro_agent, astro_tool = await create_astro_agent()
    router_agent = create_router_agent()
    img_agent = create_img_agent()
    unlock_card_agent = create_card_unlock_agent()
    return Agents(
        taro_agent=taro_agent, 
        taro_tool=taro_tool, 
        astro_agent=astro_agent, 
        astro_tool=astro_tool,
        router_agent=router_agent, 
        img_agent=img_agent,
        unlock_card_agent=unlock_card_agent
        )