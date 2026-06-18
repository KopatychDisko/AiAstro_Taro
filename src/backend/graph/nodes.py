from langgraph.graph import StateGraph
from .routing import capped_tools_condition
from langgraph.constants import END

from zep_cloud.client import AsyncZep
from zep_cloud import Message

from langchain_core.runnables import RunnableConfig

from .agents import AgentState, create_agents
from .taro_card_mapping import extract_cards_from_messages
from dotenv import load_dotenv

import logging
import os
import asyncio

load_dotenv()

logger = logging.getLogger(__name__)


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
        except Exception:
            logger.exception("Failed to fetch Zep user context")
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
        update = {'messages': [answer], 'message_to_user': answer.content}
        if answer.tool_calls:
            update['next_node'] = 'astro_tool'
            update['tool_iterations'] = state.get('tool_iterations', 0) + 1
        else:
            update['next_node'] = 'add_memory'
        return update

    async def taro_node(state):
        answer = await agents.taro_agent.ainvoke({'messages': state['messages'], 'context': state['context']})
        update = {'messages': [answer], 'message_to_user': answer.content}
        if answer.tool_calls:
            update['next_node'] = 'taro_tool'
            update['tool_iterations'] = state.get('tool_iterations', 0) + 1
        else:
            update['next_node'] = 'img_node'
        return update

    async def img_node(state):
        taro_cards, unlock_name = extract_cards_from_messages(state["messages"])
        return {
            "taro_cards": taro_cards,
            "next_node": "add_memory",
            "unlock_name": unlock_name,
        }
    
    async def add_memory(state, config: RunnableConfig):
        session_id = config['configurable']["thread_id"]
        
        answer = await agents.summarize_agent.ainvoke({'user_message': state['user_message'], 'message_to_user': state['message_to_user']})
        
        messages_to_save = [
            Message(role='user', name=state['name'], content=answer.user_message),
            Message(role='assistant', content=answer.message_to_user),
        ]
        
        try:
            await zep.thread.add_messages(
                thread_id=session_id,
                messages=messages_to_save,
            )
        except Exception:
            logger.exception("Failed to persist messages to Zep")
        
        return {'next_node': 'END'}

    def route_from_router(state):
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

    graph.add_conditional_edges(
        'router_node',
        route_from_router,
        {'taro_node': 'taro_node', 'astro_node': 'astro_node', 'add_memory': 'add_memory'},
    )

    graph.add_conditional_edges('astro_node', capped_tools_condition, {'tools': 'astro_tool', '__end__': 'add_memory'})
    graph.add_edge('astro_tool', 'astro_node')

    graph.add_conditional_edges('taro_node', capped_tools_condition, {'tools': 'taro_tool', '__end__': 'img_node'})
    graph.add_edge('taro_tool', 'taro_node')

    graph.add_edge('img_node', 'add_memory')
    
    graph.set_finish_point('add_memory')
    
    return graph.compile()
    
if __name__ == '__main__':
    compiled = asyncio.run(setup_workflow())
    print(compiled.get_graph().draw_mermaid())