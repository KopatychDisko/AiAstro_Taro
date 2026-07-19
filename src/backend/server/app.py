from contextlib import asynccontextmanager
import logging

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from server.auth import verify_stream_api_key
from server.observability import build_langfuse_callbacks
from server.schemas import ExtractData, UserData
from agents import setup_workflow

logger = logging.getLogger(__name__)


async def stream_agent(item: UserData):
    config = RunnableConfig(
        configurable={
            "thread_id": item.user_id
        },
        callbacks=build_langfuse_callbacks(item.user_id, item.name),
    )
    
    info = {
        'messages': [HumanMessage(item.message)], 
        'next_node': 'router_node', 
        'birth_day': item.birth_day, 
        'city': item.city, 
        'country': item.country, 
        'time_birth': item.time_birth, 
        'name': item.name
    }
    
    try:
        async for chunk in workflow.astream(input=info,
                                     stream_mode='values', config=config):
            if chunk.get('taro_cards'):
                chunk['taro_cards'] = [card.model_dump() for card in chunk.get('taro_cards')]
                
            info = ExtractData.model_validate(chunk)
            yield info.model_dump_json()
    except Exception:
        logger.exception("stream_agent failed", extra={"user_id": item.user_id})
        error_chunk = ExtractData(
            next_node='END',
            message_to_user='Sorry, the assistant encountered an error. Please try again.',
        )
        yield error_chunk.model_dump_json()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global workflow
    workflow = await setup_workflow()
    yield

app = FastAPI(lifespan=lifespan)

@app.post('/stream')
async def stream_endpoint(
    item: UserData,
    _: None = Depends(verify_stream_api_key),
):
    return StreamingResponse(stream_agent(item), media_type="application/json")
