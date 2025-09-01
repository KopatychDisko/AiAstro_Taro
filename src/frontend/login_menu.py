import streamlit as st

from database import get_user

from locales import t

if st.user.get('is_logged_in'):
    if get_user(str(st.user.sub)):
        st.switch_page('pages/app.py')
    else:
        st.switch_page('pages/user_info.py')

if "lang" not in st.session_state:
    st.session_state.lang = ""
    
col1, col2 = st.columns([5, 1])


with col2:
    st.session_state.lang = st.segmented_control(
        label='language',
        label_visibility='hidden',
        options=["en", "ru"],
        selection_mode='single',
        default='en'
    )
    
st.set_page_config(page_title=t("page_title"), page_icon="⚙️")
st.title(t('title'))

st.caption(t('caption_first'))

st.divider()

if st.button(t('login_button')):
    st.login()