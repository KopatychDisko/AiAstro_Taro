import streamlit as st

translations = {
    "en": {
        "language": "Language",
        "page_title": "AI Taro",
        "title": "Welcome to AI Taro! 🔮",
        "caption_first": (
            "✨ Welcome to Your AI-Tarot & Natal Chart Experience ✨\n\n"
            "Our AI-powered bot is ready to unveil your natal chart and provide insightful tarot readings—"
            "just a few details away:\n"
            "- City of Birth\n"
            "- Date of Birth\n"
            "- Time of Birth\n\n"
            "Let the magic of the cards and the wisdom of the stars guide your path! "
            "Provide your birth details to begin your personalized reading.\n\n"
            "✨ To start using AI Taro, please login by Google"
        ),
        "login_button": "Login by Google",
         #user info 
        "caption_second": (
            "✨ Welcome to Your AI-Tarot & Natal Chart Experience ✨\n\n"
            "Our AI-powered bot is ready to unveil your natal chart and provide insightful tarot readings—"
            "just a few details away:\n"
            "- City of Birth\n"
            "- Date of Birth\n"
            "- Time of Birth\n\n"
            "Let the magic of the cards and the wisdom of the stars guide your path! "
            "Provide your birth details to begin your personalized reading."
        ),
        "city_input": "Your city",
        "birth_day_input": "Your birthday",
        "time_birth_input": "Your time of birth",
        "accept_button": "Accept",
        "city_warning": "Incorrect name of city! Try again",
        "fields_warning": "Fill all fields or change birth date",
        # main app
        "page_title_chat": "AI Taro",
        "chat_title": "AI Taro Chat 🔮",
        "sidebar_title": "Settings 🛠️",
        "user_info": "User info",
        "update_data": "Update data",
        "logout_button": "Logout 😞",
        "new_data": "New data add successfully!",
        "chat_input": "Your query:",
        "think": "Think...",
        "status_taro_node": "Shuffling the cards...",
        "status_taro_tool": "What the cards say about you...",
        "status_astro_node": "Looking at the stars...",
        "status_img_node": "Laying the cards on the table...",
        "status_end": "You are ready to know your destiny",
        "error_saving_user_message": "Error saving message: {}",
        "error_saving_bot_message": "Error saving bot message: {}",
        #footer
        "created_by": "Created by Serov Egor - ",
        "get_in_touch": "If you enjoyed using this bot and want your own AI agent or automation, just get in touch! =)",
        "contact": "Contact the developer",
    },
    "ru": 
    {
        "language": "Язык",
        "page_title": "AI Таро",
        "title": "Добро пожаловать в AI Таро! 🔮",
        "caption_first": (
            "✨ Добро пожаловать в Ваш опыт AI-Таро и Натальной Карты ✨\n\n"
            "Наш AI-бот готов раскрыть Вашу натальную карту и предоставить информативные расклады таро — "
            "всё, что нужно, это заполнить несколько данных:\n"
            "- Город рождения\n"
            "- Дата рождения\n"
            "- Время рождения\n\n"
            "Пусть магия карт и мудрость звезд направляют Ваш путь! "
            "Введите данные о рождении, чтобы начать персональный расклад.\n\n"
            "✨ Чтобы начать использовать AI Таро, пожалуйста, войдите через Google"
        ),
        "login_button": "Войти через Google",
        #user info
        "page_title": "Регистрация",
        "title": "Добро пожаловать в AI Таро! 🔮",
        "caption_second": (
            "✨ Добро пожаловать в Ваш опыт AI-Таро и Натальной Карты ✨\n\n"
            "Наш AI-бот готов раскрыть Вашу натальную карту и предоставить информативные расклады таро — "
            "всё, что нужно, это заполнить несколько данных:\n"
            "- Город рождения\n"
            "- Дата рождения\n"
            "- Время рождения\n\n"
            "Пусть магия карт и мудрость звезд направляют Ваш путь! "
            "Введите данные о рождении, чтобы начать персональный расклад."
        ),
        "city_input": "Ваш город",
        "birth_day_input": "Ваша дата рождения",
        "time_birth_input": "Ваше время рождения",
        "accept_button": "Продолжить",
        "city_warning": "Некорректное название города! Попробуйте снова",
        "fields_warning": "Заполните все поля или измените дату рождения",
        # main app
        "page_title_chat": "AI Таро",
        "chat_title": "Чат AI Таро 🔮",
        "sidebar_title": "Настройки 🛠️",
        "user_info": "Информация о пользователе",
        "update_data": "Обновить данные",
        "new_data": "Новая информация успешно добавлена!",
        "logout_button": "Выйти 😞",
        "chat_input": "Ваш запрос:",
        "think": "Размышляю...",
        "status_taro_node": "Перемешиваю карты...",
        "status_taro_tool": "Что говорят карты о тебе...",
        "status_astro_node": "Смотрю на звезды...",
        "status_img_node": "Выкладываю карты на стол...",
        "status_end": "Ты готов(a) узнать свою судьбу",
        "error_saving_user_message": "Ошибка при сохранении сообщения: {}",
        "error_saving_bot_message": "Ошибка при сохранении сообщения: {}",
        #footer
        "created_by": "Сделал Егор Серов - ",
        "get_in_touch": "Если вам понравилось пользоваться этим ботом и вы хотите иметь собственного ИИ‑агента или автоматизацию, просто свяжитесь с мной! =)",
        "contact": "Связь с разработчиком"
    
    }
}

def t(key):
    return translations[st.session_state.lang].get(key, key)