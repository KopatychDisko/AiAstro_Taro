import asyncio
import sys

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from schemas import ExtractData, UserData
from graph import *
from dotenv import load_dotenv

import os


async def stream_agent(item: UserData):
    config = RunnableConfig(
        configurable={
            "thread_id": item.user_id
        }
    )
    
    async for chunk in workflow.astream({'messages': [HumanMessage(item.message)], 'next_node': 'router_node'},
                                 stream_mode='values', config=config):
        if chunk.get('taro_cards'):
            chunk['taro_cards'] = [card.model_dump() for card in chunk.get('taro_cards')]
            
        info = ExtractData.model_validate(chunk)
        yield info.model_dump_json()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    load_dotenv()
    sql_url = os.getenv('SQL_URL')
    
    async with AsyncPostgresSaver.from_conn_string(sql_url) as checkpointer:
        global workflow
        workflow = await setup_workflow(checkpointer)
        app.state.checkpointer = checkpointer
        yield

app = FastAPI(lifespan=lifespan)

@app.post('/stream')
async def stream_endpoint(item: UserData):
    return StreamingResponse(stream_agent(item), media_type="application/json")