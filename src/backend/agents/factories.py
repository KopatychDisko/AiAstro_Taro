from agents.astro.factory import create_astro_agent
from agents.cards.factory import create_card_unlock_agent
from agents.memory.factory import create_summarize_agent
from agents.router.factory import create_router_agent
from agents.state import Agents
from agents.taro.factory import create_tarot_agent


async def create_agents():
    taro_agent, taro_tool = await create_tarot_agent()
    astro_agent, astro_tool = await create_astro_agent()
    router_agent = create_router_agent()
    unlock_card_agent = create_card_unlock_agent()
    summarize_agent = create_summarize_agent()
    return Agents(
        taro_agent=taro_agent,
        taro_tool=taro_tool,
        astro_agent=astro_agent,
        astro_tool=astro_tool,
        router_agent=router_agent,
        unlock_card_agent=unlock_card_agent,
        summarize_agent=summarize_agent,
    )
