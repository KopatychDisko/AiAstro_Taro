from pydantic import BaseModel
from typing import Optional, Literal, List

class TaroCard(BaseModel):
    name: str
    reversed: bool
    
class ExtractData(BaseModel):
    message_to_user: Optional[str] = None
    taro_cards: Optional[List[TaroCard]] = None
    next_node: Optional[Literal['astro_node', 'taro_node', 'astro_tool', 'taro_tool', 'router_node','img_node', 'add_memory', 'END']] = 'router_node'
    unlock_name: Optional[str] = None
    
    class Config:
        extra = "ignore"
        
class UserData(BaseModel):
    message: str
    user_id: str
    
    birth_day: str
    time_birth: str
    city: str
    country: str
    name: str