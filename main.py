import streamlit as st
import httpx
import time

from pydantic import BaseModel
from typing import Literal, Optional, List

class TaroCard(BaseModel):
    name: str
    reversed: bool
    
class ExtractData(BaseModel):
    message_to_user: Optional[str] = None
    taro_cards: Optional[List[TaroCard]] = None
    next_node: Optional[Literal['astro_node', 'taro_node', 'astro_tool', 'taro_tool', 'router_node','img_node', 'END']] = 'router_node'
    
    class Config:
        extra = "ignore"

st.title("AI Stream Chat")

def stream_data(text):
    for word in text.split():
        yield word
        time.sleep(0.01)
        
        
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
if 'wait' not in st.session_state:
    st.session_state.wait = False
    
for msg in st.session_state.messages:
    role = msg['role']
    with st.chat_message(role):
        st.write(msg['content'])

if prompt := st.chat_input("Your query:", disabled=st.session_state.wait):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.session_state.wait = True
    
    with st.status('Think what to do....', expanded=True) as status:
        # Асинхронный запрос к FastAPI с чтением потока
        with httpx.stream("POST", "http://127.0.0.1:8000/stream", json={"message": prompt}, timeout=None) as r:
            for chunk in r.iter_text():
                data = ExtractData.model_validate_json(chunk)
                
                next_node = data.next_node
                
                if next_node == 'taro_node':
                    status.update(label='Перемешиваю карты', state='running')
                elif next_node == 'taro_tool':
                    status.update(label='Что говорят карты о тебе...', state='running')
                elif next_node == 'astro_node':
                    status.update(label='Смотрю на звезды', state='running')
                elif next_node == 'img_node':
                    status.update(label='Выкладываю карты на стол', state='running')
                elif next_node == 'END':
                    status.update(label='Ты готов(a) узнать свою судьбу', state='complete')
                    
                    msg = data.message_to_user
                    
                    st.session_state.messages.append({'role': 'ai', 'content': msg})
                    st.session_state.wait = False