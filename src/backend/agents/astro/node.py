from langchain_core.runnables import RunnableConfig


def create_astro_node(agents):
    async def astro_node(state, config: RunnableConfig):
        answer = await agents.astro_agent.ainvoke(
            {
                'messages': state['messages'],
                'birth_day': state['birth_day'],
                'time_birth': state['time_birth'],
                'city': state['city'],
                'country': state['country'],
                'context': state['context'],
            },
            config=config,
        )
        update = {'messages': [answer], 'message_to_user': answer.content}
        if answer.tool_calls:
            update['next_node'] = 'astro_tool'
            update['tool_iterations'] = state.get('tool_iterations', 0) + 1
        else:
            update['next_node'] = 'add_memory'
        return update

    return astro_node
