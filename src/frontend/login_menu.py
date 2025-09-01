import streamlit as st

from database import get_user
from footer import create_footer

from locales import t


st.set_page_config(page_title='AI Taro', page_icon="🔮")

st.markdown(
    """
    <head>
        <meta name="description" content="AI Astro Tarot — ваш персональный гид по картам таро и астрологии.">
        <meta name="keywords" content="таро, астрология, гороскоп, гадание, карты">
        <meta property="og:title" content="AI Astro Tarot — таро и астрология онлайн">
        <meta property="og:description" content="Узнайте своё будущее с помощью карт таро и астрологии.">
        <meta property="og:type" content="website">
    </head>
    """,
    unsafe_allow_html=True
)

if st.user.get('is_logged_in'):
    if get_user(str(st.user.sub)):
        st.switch_page('pages/app.py')
    else:
        st.switch_page('pages/user_info.py')
    
col1, col2 = st.columns([5, 1])


with col2:
    st.session_state.lang = st.segmented_control(
        label='language',
        label_visibility='hidden',
        options=["en", "ru"],
        selection_mode='single',
        default='en'
    )

st.title(t('title'))

st.caption(t('caption_first'))

st.divider()

if st.button(t('login_button')):
    st.login()
    
create_footer(t('created_by'), t('get_in_touch'))