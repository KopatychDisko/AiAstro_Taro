import streamlit as st
from datetime import date
from pages.check_city import get_info_from_city
from database.request import add_user


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


def check_state() -> bool:
    # Отладочная информация
    print(f"🔍 check_state() - city: {st.session_state.get('city')}")
    print(f"🔍 check_state() - time_birth: {st.session_state.get('time_birth')}")
    print(f"🔍 check_state() - birth_day: {st.session_state.get('birth_day')}")
    
    if st.session_state.get("birth_day"):
        print(f"🔍 check_state() - is_age_ok: {is_age_ok(st.session_state.birth_day)}")
    
    return (
        st.session_state.get("city")
        and st.session_state.get("time_birth")
        and st.session_state.get("birth_day")
        and is_age_ok(st.session_state.birth_day)
    )


st.set_page_config(page_title="Registration", page_icon="⚙️")
st.title("Welcome to AI Taro! 🔮")

st.caption(
    """
✨ To start using AI Taro, please login by google

"""
)

with st.container(border=True, horizontal_alignment="center", vertical_alignment="center", gap="small"):
    if st.button('Login by google'):
        st.login()