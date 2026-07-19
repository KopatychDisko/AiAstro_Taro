from langchain_core.runnables import RunnableConfig


def create_router_node(agents):
    async def router_node(state, config: RunnableConfig):
        answer = await agents.router_agent.ainvoke(
            {'messages': state['messages'], 'context': state['context']},
            config=config,
        )
        user_message = state['messages'][-1].content

        if answer.next_node == 'add_memory':
            return {
                'message_to_user': answer.message,
                'next_node': answer.next_node,
                'user_message': user_message,
            }

        return {'next_node': answer.next_node, 'user_message': user_message}

    return router_node


def route_from_router(state):
    return state['next_node']
