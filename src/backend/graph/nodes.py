from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.constants import END

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from .agents import *

async def setup_workflow():
    agents = await create_agents()
    
    async def router_node(state):
        answer = await agents.router_agent.ainvoke(state['messages'])
        
        if answer.next_node == 'END':
            return {'message_to_user': answer.message, 'next_node': answer.next_node}
        
        return {'next_node': answer.next_node}

    async def astro_node(state):
        answer = await agents.astro_agent.ainvoke(state['messages'])
        
        next_node = 'END'
        
        if answer.tool_calls:
            next_node = 'astro_tool'
        
        return {'messages': [answer], 'message_to_user': answer.content, 'next_node': next_node}

    async def taro_node(state):
        answer = await agents.taro_agent.ainvoke(state['messages'])
        
        next_node = 'img_node'
        
        if answer.tool_calls:
            next_node = 'taro_tool'
        
        return {'messages': [answer], 'message_to_user': answer.content, 'next_node': next_node}

    async def img_node(state):
        answer = await agents.img_agent.ainvoke(state['message_to_user'])
        
        return {'taro_cards': answer.taro_cards, 'next_node': 'END'}

    def next_node(state):
        return state['next_node']
    
  
    graph = StateGraph(AgentState)

    graph.add_node('router_node', router_node)
    graph.add_node('astro_node', astro_node)
    graph.add_node('taro_node', taro_node)
    graph.add_node('img_node', img_node)

    graph.add_node('taro_tool', agents.taro_tool)
    graph.add_node('astro_tool', agents.astro_tool)

    graph.set_entry_point('router_node')
    graph.add_edge('router_node', END)

    graph.add_conditional_edges('router_node', next_node, {'taro_node': 'taro_node', 'astro_node': 'astro_node', 'END': END})
        
    graph.add_edge('astro_node', END)

    graph.add_conditional_edges('astro_node', tools_condition, {'tools': 'astro_tool', '__end__': END})
    graph.add_edge('astro_tool', 'astro_node')

    graph.add_conditional_edges('taro_node', tools_condition, {'tools': 'taro_tool', '__end__': 'img_node'})
    graph.add_edge('taro_tool', 'taro_node')

    graph.add_edge('img_node', END)
    
    workflow = graph.compile()
    
    return workflow