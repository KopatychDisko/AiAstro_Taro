import streamlit as st
import time
import httpx
from datetime import date, time as dtime
from check_city import get_info_from_city
from database.request import get_last_messages, get_user, update_user, add_user

from datetime import datetime

from locales import t

from zep_cloud.client import Zep
from dotenv import load_dotenv
import os

load_dotenv()

zep_api = os.getenv('ZEP_API')

zep = Zep(api_key=zep_api)


def stream_text(text, delay=0.01):
    """Генератор, который выдаёт текст по кусочкам"""
    for char in text:
        yield char
        time.sleep(delay)


def set_data():
    user_id = str(st.user.sub)
    print(f"🔍 set_data() вызвана для пользователя: {user_id}")
    
    if "messages" not in st.session_state:
        try:
            st.session_state.messages = get_last_messages(user_id, 6)
        except:
            st.session_state.messages = []
            
    if 'city' not in st.session_state or 'country' not in st.session_state:
        try:
            user_info = get_user(user_id)
            
            if user_info:
                # Получаем данные до закрытия сессии
                st.session_state.city = user_info.city
                st.session_state.country = user_info.country
                st.session_state.birth_day = user_info.birth_date
                st.session_state.time_birth = user_info.birth_time
                st.session_state.lang = user_info.language
                
                # Отладочная информация
                print(f"📥 Загружены данные пользователя: {user_info.user_id}")
                print(f"   Город: {user_info.city}")
                print(f"   Страна: {user_info.country}")
                print(f"   Дата рождения: {user_info.birth_date}")
                print(f"   Время рождения: {user_info.birth_time}")
            else:
                print(f"❌ Пользователь {user_id} не найден в базе данных")
        except Exception as e:
            print(f"Error loading user info: {e}")

    if "wait" not in st.session_state:
        st.session_state.wait = False

    if "ai_msg" not in st.session_state:
        st.session_state.ai_msg = ""

    if "user_avatar" not in st.session_state and hasattr(st, "user") and st.user.picture:
        try:
            user_avatar_url = st.user.picture
            r = httpx.get(user_avatar_url)
            st.session_state.user_avatar = r.content
        except Exception as e:
            print(f"Error loading avatar: {e}")

    if "bot_avatar" not in st.session_state:
        st.session_state.bot_avatar = "images/bot_avatar.png"


def create_form_with_info():
    with st.form(key="unique_info"):
        city = st.text_input(t('city_input'), value=st.session_state.city)

        birth_day = st.date_input(
            t('birth_day_input'),
            format="DD.MM.YYYY",
            value=datetime.strptime(st.session_state.birth_day, "%d.%m.%Y").date()
        )
        
        # Стримлит требует дефолт → ставим полночь
        time_birth = st.time_input(t('time_birth_input'), value=datetime.strptime(st.session_state.time_birth, "%H:%M").time())

        submit = st.form_submit_button(t('update_data'))

        if submit:
            city_info = get_info_from_city(city) if city else None

            if city_info:
                st.session_state.city = city_info[0]
                st.session_state.country = city_info[1]
                st.session_state.birth_day = birth_day.strftime("%d.%m.%Y")
                st.session_state.time_birth = time_birth.strftime("%H:%M")

                st.success(t('new_data'))
                
                try:
                    update_user(str(st.user.sub), st.session_state.birth_day, st.session_state.time_birth, st.session_state.city, st.session_state.country)
                except Exception as e:
                    add_user(str(st.user.sub), st.session_state.birth_day, st.session_state.time_birth, st.session_state.city, st.session_state.country)
            else:
                st.warning(t('fields_warning'))
                
def create_user_zep():
    try:
        zep.user.add(
            user_id=str(st.user.sub),
            first_name=st.user.given_name,
            email=st.user.email,
        )
        
        zep.thread.create(
            thread_id=str(st.user.sub),
            user_id=str(st.user.sub)
        )
    except:
        print(f'User_id {str(st.user.sub)} already exist')