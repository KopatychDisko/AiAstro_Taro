from pydantic import BaseModel


class TaroCard(BaseModel):
    name: str
    reversed: bool
