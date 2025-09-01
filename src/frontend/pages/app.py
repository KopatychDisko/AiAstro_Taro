import streamlit as st
import httpx
import json

from schema import *
from templates import create_html_taro

from utils import stream_text, set_data, create_form_with_info
from database.request import add_message

from locales import t


if not st.user.is_logged_in:
    st.switch_page('login_menu.py')
    
set_data()

col_1, col_2 = st.columns([5, 1])
with col_2:
    lang = st.segmented_control(
        label=t('language'),
        label_visibility='hidden',
        options=["en", "ru"],
        selection_mode='single',
        default=st.session_state.lang
    )
    
    st.session_state.lang = lang

st.set_page_config(page_title=t('page_title_chat'), page_icon='🔮')
st.title(t('chat_title'))

    
for msg in st.session_state.messages:
    avatar = st.session_state.user_avatar if msg['role'] == 'user' else st.session_state.bot_avatar
    with st.chat_message(msg['role'], avatar=avatar):
        if msg.get('cards'):
            create_html_taro(msg['cards'], msg['unlock_name'])    
        st.markdown(msg['content'])
        
with st.sidebar:
    st.title(t('sidebar_title'))
    
    st.divider()
    
    st.subheader(t('user_info'))
    create_form_with_info()
    
    st.divider()
    
    if st.user.is_logged_in:
        if st.button(t('logout_button')):
            st.logout()
            
    st.divider()
    
    with st.popover(t('contact')):
        st.markdown("""
    - [GitHub](https://github.com/KopatychDisko)  
    - [Telegram](https://t.me/eserov73)  
    - eserov73@gmail.com  
    """, unsafe_allow_html=True)
    
    
prompt = st.chat_input(t('chat_input'), key='chat_input', disabled=st.session_state.wait)

if prompt:
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message("user", avatar=st.session_state.user_avatar):
        st.markdown(prompt)
        add_message(st.user.sub, 'user', prompt)
        
    st.session_state.wait = True
    
        
if st.session_state.wait:  
    with st.status(t('think')) as status:
        # Асинхронный запрос к FastAPI с чтением потока
        request_data = {
            "message": prompt, 
            "user_id": str(st.user.sub), 
            "country": st.session_state.country, 
            "time_birth": st.session_state.time_birth, 
            "birth_day": st.session_state.birth_day, 
            "city": st.session_state.city,
            "name": st.user.given_name
            }
        
        with httpx.stream("POST", "http://127.0.0.1:8000/stream", json=request_data, timeout=None) as r:
            for chunk in r.iter_text():
                temp = json.loads(chunk)
                data = ExtractData.model_validate(temp)
                
                next_node = data.next_node
                
                if next_node == 'taro_node':
                    status.update(label=t('status_taro_node'), state='running')
                elif next_node == 'taro_tool':
                    status.update(label=t('status_taro_tool'), state='running')
                elif next_node == 'astro_node':
                    status.update(label=t('status_astro_node'), state='running')
                elif next_node == 'img_node':
                    status.update(label=t('status_img_node'), state='running')
                elif next_node == 'END':
                    status.update(label=t('status_end'), state='complete')
                    
                    st.session_state.ai_msg = data.message_to_user
                    
                    st.session_state.cards = data.taro_cards
                    st.session_state.unlock_name = data.unlock_name
                    
                    st.session_state.messages.append({'role': 'ai', 'content': st.session_state.ai_msg, 'cards': st.session_state.cards, 'unlock_name': st.session_state.unlock_name})
    
    with st.chat_message('ai', avatar=st.session_state.bot_avatar):
        if st.session_state.get('cards'):
            html_code = create_html_taro(st.session_state.cards, 
                            st.session_state.unlock_name)
        add_message(st.user.sub, 'bot', st.session_state.ai_msg)
        st.write_stream(stream_text(st.session_state.ai_msg))
        
    st.session_state.cards = None
    st.session_state.wait = False
    
    st.rerun()