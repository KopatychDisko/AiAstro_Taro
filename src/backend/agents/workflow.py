from langgraph.graph import StateGraph
from zep_cloud.client import AsyncZep
from zep_cloud import Message
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv

import logging
import os
import asyncio

from agents.factories import create_agents
from agents.state import AgentState
from agents.routing import capped_tools_condition
from agents.router.node import create_router_node, route_from_router
from agents.taro.node import create_taro_node
from agents.astro.node import create_astro_node
from agents.cards.node import img_node

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

    async def add_memory(state, config: RunnableConfig):
        session_id = config['configurable']["thread_id"]

        answer = await agents.summarize_agent.ainvoke(
            {
                'user_message': state['user_message'],
                'message_to_user': state['message_to_user'],
            },
            config=config,
        )

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

    router_node = create_router_node(agents)
    astro_node = create_astro_node(agents)
    taro_node = create_taro_node(agents)

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

    graph.add_conditional_edges(
        'astro_node',
        capped_tools_condition,
        {'tools': 'astro_tool', '__end__': 'add_memory'},
    )
    graph.add_edge('astro_tool', 'astro_node')

    graph.add_conditional_edges(
        'taro_node',
        capped_tools_condition,
        {'tools': 'taro_tool', '__end__': 'img_node'},
    )
    graph.add_edge('taro_tool', 'taro_node')

    graph.add_edge('img_node', 'add_memory')

    graph.set_finish_point('add_memory')

    return graph.compile()


if __name__ == '__main__':
    compiled = asyncio.run(setup_workflow())
    print(compiled.get_graph().draw_mermaid())
