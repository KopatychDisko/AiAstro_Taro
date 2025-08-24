import streamlit as st
import httpx
import time
import json

from schema import *
from templates import render_celtic_cross

def stream_text(text, delay=0.01):
    """Генератор, который выдаёт текст по кусочкам"""
    for char in text:
        yield char
        time.sleep(delay)
            
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
if 'wait' not in st.session_state:
    st.session_state.wait = False
    
if 'ai_msg' not in st.session_state:
    st.session_state.ai_msg = ''

st.title("AI Stream Chat")   
    
for  msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        if msg.get('cards'):
            render_celtic_cross(msg['cards'])
            
        st.markdown(msg['content'])
        
if prompt := st.chat_input("Your query:", disabled=st.session_state.wait):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.session_state.wait = True
    
    with st.status('Think...') as status:
        # Асинхронный запрос к FastAPI с чтением потока
        with httpx.stream("POST", "http://127.0.0.1:8000/stream", json={"message": prompt}, timeout=None) as r:
            for chunk in r.iter_text():
                temp = json.loads(chunk)
                data = ExtractData.model_validate(temp)
                
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
                    
                    st.session_state.ai_msg = data.message_to_user
                    
                    st.session_state.cards = data.taro_cards if data.taro_cards else None
                    
                    st.session_state.messages.append({'role': 'ai', 'content': st.session_state.ai_msg, 'cards': st.session_state.cards})
                    
    if st.session_state.cards:
        render_celtic_cross(st.session_state.cards)
    
    with st.chat_message('ai'):
        st.write_stream(stream_text(st.session_state.ai_msg))
        
    st.session_state.cards = None
    st.session_state.wait = False
    st.rerun()