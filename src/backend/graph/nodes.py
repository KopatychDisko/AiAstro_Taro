from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.constants import END

from zep_cloud.client import AsyncZep
from zep_cloud import Message

from langchain_core.runnables import RunnableConfig

from .agents import *
from dotenv import load_dotenv

import os
import asyncio

load_dotenv()


async def setup_workflow():
    agents = await create_agents()
    
    zep_api = os.getenv('ZEP_API')
    
    zep = AsyncZep(api_key=zep_api)
    
    async def take_context(state, config: RunnableConfig):
        session_id = config['configurable']["thread_id"]
        user_name = state['name']
        
        try:
            memory = await zep.thread.get_user_context(session_id)
            context = f'User name: {user_name}\n Context: {memory.context}'
        except:
            context = f'User name: {user_name}'
         
        return {'context': context}
    
    async def router_node(state):
        answer = await agents.router_agent.ainvoke({'messages': state['messages'], 'context': state['context']})
        user_message = state['messages'][-1].content
        
        if answer.next_node == 'add_memory':
            return {'message_to_user': answer.message, 'next_node': answer.next_node, 'user_message': user_message}
    
        return {'next_node': answer.next_node, 'user_message': user_message}

    async def astro_node(state):
        answer = await agents.astro_agent.ainvoke({'messages': state['messages'], 'birth_day': state['birth_day'], 'time_birth': state['time_birth'], 'city': state['city'], 'country': state['country'], 'context': state['context']})
        next_node = 'add_memory'
        
        if answer.tool_calls:
            next_node = 'astro_tool'
        
        return {'messages': [answer], 'message_to_user': answer.content, 'next_node': next_node}

    async def taro_node(state):
        answer = await agents.taro_agent.ainvoke({'messages': state['messages'], 'context': state['context']})
        
        next_node = 'img_node'
        
        if answer.tool_calls:
            next_node = 'taro_tool'
        
        return {'messages': [answer], 'message_to_user': answer.content, 'next_node': next_node}

    async def img_node(state):
        answer = await agents.img_agent.ainvoke(state['message_to_user'])
        
        return {'taro_cards': answer.taro_cards, 'next_node': 'add_memory', 'unlock_name': answer.unlock_name}
    
    async def add_memory(state, config: RunnableConfig):
        session_id = config['configurable']["thread_id"]
        
        answer = await agents.summarize_agent.ainvoke({'user_message': state['user_message'], 'message_to_user': state['message_to_user']})
        
        messages_to_save = [
            Message(role='user', name=state['name'], content=answer.user_message),
            Message(role='assistant', content=answer.message_to_user),
        ]
        
        await zep.thread.add_messages(
        thread_id=session_id,
        messages=messages_to_save,
        )
        
        return {'next_node': 'END'}

    def next_node(state):
        return state['next_node']
    
  
    graph = StateGraph(AgentState)

    graph.add_node('router_node', router_node)
    graph.add_node('astro_node', astro_node)
    graph.add_node('taro_node', taro_node)
    graph.add_node('img_node', img_node)

    graph.add_node('taro_tool', agents.taro_tool)
    graph.add_node('astro_tool', agents.astro_tool)
    
    graph.add_node('take_context', take_context)
    graph.add_node('add_memory', add_memory)

    graph.set_entry_point('take_context')
    graph.add_edge('take_context', 'router_node')

    graph.add_conditional_edges('router_node', next_node, {'taro_node': 'taro_node', 'astro_node': 'astro_node', 'add_memory': 'add_memory'})
        
    graph.add_edge('astro_node', 'add_memory')

    graph.add_conditional_edges('astro_node', tools_condition, {'tools': 'astro_tool', '__end__': 'add_memory'})
    graph.add_edge('astro_tool', 'astro_node')

    graph.add_conditional_edges('taro_node', tools_condition, {'tools': 'taro_tool', '__end__': 'img_node'})
    graph.add_edge('taro_tool', 'taro_node')

    graph.add_edge('img_node', 'add_memory')
    
    graph.set_finish_point('add_memory')
    
    return graph.compile()
    
if __name__ == '__main__':
    graph = asyncio.run(setup_workflow())
    graph.draw_mermaid()