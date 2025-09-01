import streamlit as st
from datetime import date
from check_city import get_info_from_city
from database.request import add_user, update_user

from locales import t

from utils import create_user_zep

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
    
if 'lang' not in st.session_state:
    st.session_state.lang = ''

col1, col2 = st.columns([5, 1])

with col2:
    lang = st.segmented_control(
        label='language',
        label_visibility='hidden',
        options=["en", "ru"],
        selection_mode='single',
        default='en'
    )
    
    st.session_state.lang = lang
    
st.title(t('title'))

st.caption(t('caption_second'))

with st.container(border=True, horizontal_alignment="center", vertical_alignment="center", gap="small"):
    st.session_state.city = st.text_input(t('city_input'))

    st.session_state.birth_day = st.date_input(
        t('birth_day_input'),
        format="DD.MM.YYYY",
        max_value=thirteen_years_ago,
        min_value=ninety_years_ago,
    )

    st.session_state.time_birth = st.time_input(t('time_birth_input'), step=60)
    
    st.divider()
    
    if st.button(t('accept_button')):
        if check_state():
            try:
                city, country = get_info_from_city(st.session_state.city)
            except:
                city = None
            if city:
                try:
                    add_user(str(st.user.sub), st.session_state.birth_day.strftime("%d.%m.%Y"), st.session_state.time_birth.strftime("%H:%M"), city, country, st.session_state.lang)
                except:
                    update_user(str(st.user.sub), st.session_state.birth_day.strftime("%d.%m.%Y"), st.session_state.time_birth.strftime("%H:%M"), city, country, st.session_state.lang)
                finally:
                    create_user_zep()
                    st.switch_page('pages/app.py')
            else:
                st.warning(t('city_warning'))
        else:
            st.warning(t('fields_warning'))
            