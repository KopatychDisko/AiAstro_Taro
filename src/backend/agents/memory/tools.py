from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from zep_cloud.client import AsyncZep

from agents.config import zep_api

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
