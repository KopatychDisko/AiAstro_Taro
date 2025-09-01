from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from schemas import ExtractData, UserData
from graph import *


async def stream_agent(item: UserData):
    config = RunnableConfig(
        configurable={
            "thread_id": item.user_id
        }
    )
    
    info = {
        'messages': [HumanMessage(item.message)], 
        'next_node': 'router_node', 
        'birth_day': item.birth_day, 
        'city': item.city, 
        'country': item.city, 
        'time_birth': item.time_birth, 
        'name': item.name
    }
    
    async for chunk in workflow.astream(input=info,
                                 stream_mode='values', config=config):
        if chunk.get('taro_cards'):
            chunk['taro_cards'] = [card.model_dump() for card in chunk.get('taro_cards')]
            
        info = ExtractData.model_validate(chunk)
        yield info.model_dump_json()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global workflow
    workflow = await setup_workflow()
    yield

app = FastAPI(lifespan=lifespan)

@app.post('/stream')
async def stream_endpoint(item: UserData):
    return StreamingResponse(stream_agent(item), media_type="application/json")