import streamlit as st
from datetime import datetime, timedelta, date

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
    return age >= 13 and age <= 90

def check_state(): 
    return st.session_state.get('city') and st.session_state.get('time_birth') and st.session_state.get('birth_day') and is_age_ok(st.session_state.birth_day)
    
st.set_page_config(page_title='Registration', page_icon='⚙️')
st.title('Welcome to AI Taro! 🔮')

st.caption('''
✨ To start using AI Taro, we need some information to create your natal chart.
📝 Please fill in the form below:
 - Date of birth
 - Place of birth
 - Time of birth

⏳ If you don’t know your exact time of birth, just enter an approximate time — it will still allow us to generate your chart.
''')

with st.container(border=True, horizontal_alignment='center', vertical_alignment='center', gap='small'):
    if city := st.text_input("Your city"):
        st.session_state.city = city

    if birth_day := st.date_input("Your birthday", format="DD.MM.YYYY", max_value=thirteen_years_ago, value=thirteen_years_ago, min_value=ninety_years_ago):
        st.session_state.birth_day = birth_day


    if time_birth := st.time_input('Your time birth'):
        st.session_state.time_birth = time_birth
        
    st.divider()

    if st.button('Login by Google', type='secondary'):
        if check_state():
            st.login()
        else:
            st.warning('Fill all filed please or write valid data!')
            
if st.user.is_logged_in:
    st.switch_page('app.py')

