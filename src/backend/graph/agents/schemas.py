from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

from typing import Literal, Optional, List, Dict

class RouterOutput(BaseModel):
    next_node: Literal['astro_node', 'taro_node', 'add_memory'] = Field(..., description='What next node need ot execute')
    
    message: Optional[str] = Field(description='If you need just answer user')
    
class TaroCard(BaseModel):
    name: str
    reversed: bool
    
class AgentState(MessagesState):
    next_node: Literal['astro_node', 'taro_node', 'astro_tool', 'taro_tool', 'add_memory', 'END'] = Field(..., description='What next node need ot execute')
    
    taro_cards: List[TaroCard]
    unlock_name: str
    
    message_to_user: str
    user_message: str
    context: str
    
    birth_day: str
    time_birth: str
    city: str
    country: str
    name: str
    
class ImgOutput(BaseModel):
    taro_cards: List[TaroCard] = Field(..., description='Fill this with name of taro card and reversed (bool)')
    
    unlock_name: str = Field(..., description='Name of unlock card')
    
    
class UnlockCard(BaseModel):
    unlock_name: str = Field(..., description='Name of unlock card')
    
class Summarize(BaseModel):
    user_message: str
    message_to_user: str = Field(..., description='Ai message')
    
class Agents(BaseModel):
    taro_agent: object
    taro_tool: object
    astro_agent: object
    astro_tool: object
    router_agent: object
    img_agent: object
    unlock_card_agent: object
    summarize_agent: object

    model_config = {
        "arbitrary_types_allowed": True
    }
    