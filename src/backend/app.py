from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage

from schemas import ExtractData, UserMessage, TaroCard
from graph import *

async def stream_agent(message):
    input_state = {"configurable": {"thread_id": "1"}}
    async for chunk in workflow.astream({'messages': [HumanMessage(message)]},
                                 stream_mode='values'):
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
    # Shutdown

app = FastAPI(lifespan=lifespan)

@app.post('/stream')
async def stream_endpoint(item: UserMessage):
    msg = item.message
    return StreamingResponse(stream_agent(msg), media_type="application/json")