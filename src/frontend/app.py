import streamlit as st
import httpx
import json

from schema import *
from templates import create_html_taro

from utils import stream_text, set_data, create_form_with_info
from database.request import add_message, get_user, get_last_messages



if not st.user.is_logged_in:
    st.switch_page('pages/login_menu.py')
    
set_data()

st.set_page_config(page_title='AI Taro', page_icon='🔮')
st.title("AI taro chat")
    
for msg in st.session_state.messages:
    avatar = st.session_state.user_avatar if msg['role'] == 'user' else st.session_state.bot_avatar
    with st.chat_message(msg['role'], avatar=avatar):
        if msg.get('cards'):
            create_html_taro(msg['cards'], msg['unlock_name'])
        st.markdown(msg['content'])
        
with st.sidebar:
    st.title('Settings 🛠️')
    
    st.divider()
    
    st.subheader('User info')
    create_form_with_info()
    
    st.divider()
    
    
    if st.user.is_logged_in:
        if st.button('Logout 😞'):
            st.logout()
    
    
prompt = st.chat_input("Your query:", key='chat_input', disabled=st.session_state.wait)

if prompt:
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message("user", avatar=st.session_state.user_avatar):
        st.markdown(prompt)
        try:
            add_message(st.user.sub, 'user', prompt)
        except Exception as e:
            st.error(f"Error saving message: {e}")
        
    st.session_state.wait = True
    
        
if st.session_state.wait:  
    with st.status('Think...') as status:
        # Асинхронный запрос к FastAPI с чтением потока
        request_data = {
            "message": prompt, 
            "user_id": st.user.sub, 
            "country": st.session_state.country, 
            "time_birth": st.session_state.time_birth, 
            "birth_day": st.session_state.birth_day, 
            "city": st.session_state.city
        }
        
        with httpx.stream("POST", "http://127.0.0.1:8000/stream", json=request_data, timeout=None) as r:
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
                    
                    st.session_state.cards = data.taro_cards
                    st.session_state.unlock_name = data.unlock_name
                    
                    st.session_state.messages.append({'role': 'ai', 'content': st.session_state.ai_msg, 'cards': st.session_state.cards, 'unlock_name': st.session_state.unlock_name})
    
    with st.chat_message('ai', avatar=st.session_state.bot_avatar):
        if st.session_state.cards:
            html_code = create_html_taro(st.session_state.cards, 
                            st.session_state.unlock_name)
            try:
                add_message(st.user.sub, 'bot', st.session_state.ai_msg, html_code)
            except Exception as e:
                st.error(f"Error saving bot message: {e}")
            
        st.write_stream(stream_text(st.session_state.ai_msg))
    st.session_state.cards = None
    st.session_state.wait = False
    
    st.rerun()