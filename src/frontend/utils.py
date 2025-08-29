import streamlit as st
import time
import httpx
from datetime import date, time as dtime
from pages.check_city import get_info_from_city

today = date.today()
thirteen_years_ago = today.replace(year=today.year - 13)

try:
    ninety_years_ago = today.replace(year=today.year - 90)
except ValueError:
    # Обработка 29 февраля в високосный год
    ninety_years_ago = today.replace(month=2, day=28, year=today.year - 90)


def is_age_ok(birth_date: date) -> bool:
    today = date.today()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    return 13 <= age <= 90


def stream_text(text, delay=0.01):
    """Генератор, который выдаёт текст по кусочкам"""
    for char in text:
        yield char
        time.sleep(delay)


def set_data():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "wait" not in st.session_state:
        st.session_state.wait = False

    if "ai_msg" not in st.session_state:
        st.session_state.ai_msg = ""

    if "user_avatar" not in st.session_state and hasattr(st, "user") and st.user.picture:
        user_avatar_url = st.user.picture
        r = httpx.get(user_avatar_url)
        st.session_state.user_avatar = r.content

    if "bot_avatar" not in st.session_state:
        st.session_state.bot_avatar = "images/bot_avatar.png"


def create_form_with_info():
    with st.form(key="unique_info"):
        city = st.text_input("Your city")

        birth_day = st.date_input(
            "Your birthday",
            format="DD.MM.YYYY",
            max_value=thirteen_years_ago,
            min_value=ninety_years_ago,
        )

        # Стримлит требует дефолт → ставим полночь
        time_birth = st.time_input("Your time birth", value=dtime(0, 0))

        submit = st.form_submit_button("Update data")

        if submit:
            city_info = get_info_from_city(city) if city else None

            if is_age_ok(birth_day) and city_info:
                st.session_state.city = city_info[0]
                st.session_state.country = city_info[1]
                st.session_state.birth_day = birth_day.strftime("%DD.%MM.%YYYY")
                st.session_state.time_birth = time_birth.strftime("%H:%M")

                st.success("New data add successfully!")
            else:
                st.warning("Fill all fields or change birth day!")

    