from langchain_core.runnables import RunnableConfig


def create_taro_node(agents):
    async def taro_node(state, config: RunnableConfig):
        answer = await agents.taro_agent.ainvoke(
            {'messages': state['messages'], 'context': state['context']},
            config=config,
        )
        update = {'messages': [answer], 'message_to_user': answer.content}
        if answer.tool_calls:
            update['next_node'] = 'taro_tool'
            update['tool_iterations'] = state.get('tool_iterations', 0) + 1
        else:
            update['next_node'] = 'img_node'
        return update

    return taro_node
