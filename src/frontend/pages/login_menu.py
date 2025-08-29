import streamlit as st
from datetime import date
from .check_city import get_info_from_city

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
✨ To start using AI Taro, we need some information to create your natal chart.
📝 Please fill in the form below:
 - Date of birth
 - Place of birth
 - Time of birth

⏳ If you don’t know your exact time of birth, just enter an approximate time — it will still allow us to generate your chart.
"""
)

with st.container(border=True, horizontal_alignment="center", vertical_alignment="center", gap="small"):
    if city := st.text_input("Your city"):
        st.session_state.city = city

    if birth_day := st.date_input(
        "Your birthday",
        format="DD.MM.YYYY",
        max_value=thirteen_years_ago,
        value=thirteen_years_ago,
        min_value=ninety_years_ago,
    ):
        st.session_state.birth_day = birth_day.strftime("%DD.%MM.%YYYY")

    if time_birth := st.time_input("Your time birth"):
        # Сохраняем СРАЗУ в строковом формате
        st.session_state.time_birth = time_birth.strftime("%H:%M")

    st.divider()

    if st.button("Login by Google", type="secondary"):
        if check_state():
            city_info = get_info_from_city(st.session_state.city)
            if city_info:
                st.session_state.city = city_info[0]
                st.session_state.country = city_info[1]
                st.login()
            else:
                st.warning("City not found, try another one.")
        else:
            st.warning("Fill all fields please or write valid data!")

if st.user.is_logged_in:
    st.switch_page("app.py")
