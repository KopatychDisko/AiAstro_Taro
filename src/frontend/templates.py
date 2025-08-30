import streamlit as st
import math

def create_git_url_images(tarot_photo: list):
    photos_urls = []
    for info in tarot_photo:
        name, reversed = info.name, info.reversed
        tarot_url = f'https://github.com/KopatychDisko/tarot_images/blob/main/images/{name}.jpeg?raw=true'
        photos_urls.append({"img": tarot_url, "reversed": reversed})
    return photos_urls

def render_celtic_cross(cards):
    cards_data = create_git_url_images(cards)

    # позиции карт в процентах (top%, left%)
    positions = [
        (50, 50), (50, 50), (50, 70), (50, 10),
        (30, 50), (70, 50), (90, 10), (90, 20),
        (90, 30), (90, 40)
    ]
    
    html_code = '''
    <div class="celtic-cross" style="
        position: relative;
        width: 100%;
        max-width: 800px;
        aspect-ratio: 4/3;
        margin: 0 auto;
    ">
    '''
    
    for i, card in enumerate(cards_data):
        top_pct, left_pct = positions[i]
        transform = "rotate(90deg)" if i == 1 else ("rotate(180deg)" if card["reversed"] else "none")
        
        html_code += f"""
        <div style="
            position:absolute;
            top:{top_pct}%;
            left:{left_pct}%;
            width:15%;
            aspect-ratio: 2/3;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """

    html_code += '</div>'

    # убираем фиксированную высоту, чтобы адаптировалось
    st.components.v1.html(html_code, height=600)  
    return html_code

    
def render_three_card(cards):
    """
    cards: список из 3 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)

    # позиции карт в процентах (от ширины и высоты контейнера)
    positions = [(50, 15), (50, 50), (50, 85)]  # top%, left%

    html_code = '''
    <div class="three-card" style="
        position: relative;
        width: 100%;
        max-width: 600px;
        aspect-ratio: 3/2;
        margin: 0 auto;
    ">
    '''

    for i, card in enumerate(cards_data):
        top_pct, left_pct = positions[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"
        html_code += f"""
        <div style="
            position: absolute;
            top: {top_pct}%;
            left: {left_pct}%;
            width: 18%;
            aspect-ratio: 2/3;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.25);
            transform: {transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """

    html_code += '</div>'

    # высота компонента можно оставить фиксированной для Streamlit, но контейнер масштабируется
    st.components.v1.html(html_code, height=400)
    
    return html_code


    
def render_horseshoe(cards):
    """
    cards: список из 7 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)
    n = len(cards_data)
    
    # Полукруг: радиус и центр
    radius = 200
    center_x, center_y = 250, 250
    start_angle = math.pi  # 180 градусов (левая сторона)
    end_angle = 0          # 0 градусов (правая сторона)

    html_code = '<div class="horseshoe" style="position:relative; width:500px; height:300px;">'
    
    for i, card in enumerate(cards_data):
        angle = start_angle + (i / (n - 1)) * (end_angle - start_angle)
        left = center_x + radius * math.cos(angle) - 60  # центрируем по ширине карты
        top = center_y + radius * math.sin(angle) - 90   # центрируем по высоте
        transform = "rotate(180deg)" if card["reversed"] else "none"
        
        html_code += f"""
        <div style="
            position:absolute;
            top:{top}px;
            left:{left}px;
            width:120px;
            height:180px;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """
    
    html_code += '</div>'
    st.components.v1.html(html_code, height=300)
    
    return html_code
    
def render_relationship(cards):
    """
    cards: список из 7 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)

    # Позиции карт в процентах (top%, left%)
    positions = [
        (20, 15),   # 1: партнер
        (20, 85),   # 2: себя
        (40, 50),   # 3: сила отношений (центр)
        (60, 50),   # 4: проблемы
        (80, 15),   # 5: совет
        (80, 85),   # 6: внешние влияния
        (95, 50),   # 7: итог
    ]

    html_code = '''
    <div class="relationship-cross" style="
        position: relative;
        width: 100%;
        max-width: 400px;
        aspect-ratio: 4/5;
        margin: 0 auto;
    ">
    '''

    for i, card in enumerate(cards_data):
        top_pct, left_pct = positions[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"

        html_code += f"""
        <div style="
            position:absolute;
            top:{top_pct}%;
            left:{left_pct}%;
            width:18%;
            aspect-ratio: 2/3;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """

    html_code += '</div>'
    st.components.v1.html(html_code, height=500)  # высота компонента Streamlit
    return html_code


def render_career_path(cards):
    """
    cards: список из 6 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)

    # Позиции карт в процентах (top%, left%)
    positions = [
        (10, 15),   # 1: текущая ситуация
        (40, 15),   # 2: сильные стороны
        (70, 15),   # 3: слабые стороны
        (10, 75),   # 4: совет
        (40, 75),   # 5: внешние влияния
        (70, 75),   # 6: результат
    ]

    html_code = '''
    <div class="career-path" style="
        position: relative;
        width: 100%;
        max-width: 520px;
        aspect-ratio: 1/1;
        margin: 0 auto;
    ">
    '''

    for i, card in enumerate(cards_data):
        top_pct, left_pct = positions[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"
        html_code += f"""
        <div style="
            position:absolute;
            top:{top_pct}%;
            left:{left_pct}%;
            width:18%;
            aspect-ratio: 2/3;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:cover;">
        </div>
        """

    html_code += '</div>'

    # Высота компонента Streamlit, можно оставить фиксированной
    st.components.v1.html(html_code, height=550)

    return html_code


def render_decision_making(cards):
    """
    cards: список из 5 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)

    # Позиции карт в процентах (top%, left%)
    positions = [
        (20, 15),   # 1: Вариант A
        (20, 55),   # 2: Вариант B
        (50, 15),   # 3: Преимущества/риски
        (50, 55),   # 4: Совет
        (80, 35),   # 5: Итог/решение
    ]

    html_code = '''
    <div class="decision-making" style="
        position: relative;
        width: 100%;
        max-width: 650px;
        aspect-ratio: 13/9;
        margin: 0 auto;
    ">
    '''

    for i, card in enumerate(cards_data):
        top_pct, left_pct = positions[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"

        html_code += f"""
        <div style="
            position:absolute;
            top:{top_pct}%;
            left:{left_pct}%;
            width:18%;
            aspect-ratio: 2/3;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """

    html_code += '</div>'

    # Высота компонента Streamlit, контейнер масштабируется
    st.components.v1.html(html_code, height=450)

    return html_code
    

def render_year_ahead(cards):
    """
    cards: список из 13 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)

    html_code = '''
    <div class="year-ahead" style="
        position: relative;
        width: 100%;
        max-width: 1400px;
        aspect-ratio: 14/3;
        margin: 0 auto;
    ">
    '''

    # карты месяцев (12 карт)
    for i in range(12):
        top_pct = 30
        left_pct = 5 + i * 7  # примерно равномерно распределяем по ширине
        card = cards_data[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"

        html_code += f"""
        <div style="
            position:absolute;
            top:{top_pct}%;
            left:{left_pct}%;
            width:6%;
            aspect-ratio: 5/8;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """

    # итоговая карта года
    card = cards_data[12]
    top_pct = 5
    left_pct = 45
    transform = "rotate(180deg)" if card["reversed"] else "none"

    html_code += f"""
    <div style="
        position:absolute;
        top:{top_pct}%;
        left:{left_pct}%;
        width:8%;
        aspect-ratio: 2/3;
        border-radius:10px;
        overflow:hidden;
        box-shadow:0 4px 8px rgba(0,0,0,0.25);
        transform:{transform};
    ">
        <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
    </div>
    """

    html_code += '</div>'

    # высота компонента Streamlit, контейнер масштабируется по ширине
    st.components.v1.html(html_code, height=300)

    return html_code



def render_spiritual(cards):
    """
    cards: список из 6 карт, каждая {"name": str, "reversed": bool}
    """
    if len(cards) != 6:
        st.error("Необходимо ровно 6 карт")
        return

    cards_data = create_git_url_images(cards)

    # Позиции карт в процентах (top%, left%)
    positions = [
        (15, 10), (15, 45), (15, 80),  # верхний ряд
        (55, 10), (55, 45), (55, 80)   # нижний ряд
    ]

    html_code = '''
    <div class="spiritual-guidance" style="
        position: relative;
        width: 100%;
        max-width: 700px;
        aspect-ratio: 2/1;
        margin: 0 auto;
    ">
    '''

    for i, card in enumerate(cards_data):
        top_pct, left_pct = positions[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"

        html_code += f"""
        <div style="
            position:absolute;
            top:{top_pct}%;
            left:{left_pct}%;
            width:18%;
            aspect-ratio: 2/3;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """

    html_code += '</div>'

    # Высота компонента Streamlit, контейнер масштабируется по ширине
    st.components.v1.html(html_code, height=350)

    return html_code


def render_chakra(cards):
    """
    cards: список из 7 карт, каждая {"name": str, "reversed": bool}
    """
    if len(cards) != 7:
        st.error("Необходимо ровно 7 карт")
        return

    cards_data = create_git_url_images(cards)

    # Позиции карт в процентах (top%, left%)
    positions = [
        (0, 15),    # Корневая
        (14, 15),   # Сакральная
        (28, 15),   # Солнечное сплетение
        (42, 15),   # Сердечная
        (56, 15),   # Горловая
        (70, 15),   # Третий глаз
        (84, 15),   # Коронная
    ]

    html_code = '''
    <div class="chakra-alignment" style="
        position: relative;
        width: 100%;
        max-width: 180px;
        aspect-ratio: 1/5;
        margin: 0 auto;
    ">
    '''

    for i, card in enumerate(cards_data):
        top_pct, left_pct = positions[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"

        html_code += f"""
        <div style="
            position:absolute;
            top:{top_pct}%;
            left:{left_pct}%;
            width:18%;
            aspect-ratio: 2/3;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """

    html_code += '</div>'

    # Высота компонента Streamlit, контейнер масштабируется
    st.components.v1.html(html_code, height=900)

    return html_code


def render_shadow(cards):
    """
    cards: список из 5 карт, каждая {"name": str, "reversed": bool}
    """
    if len(cards) != 5:
        st.error("Необходимо ровно 5 карт")
        return

    cards_data = create_git_url_images(cards)

    # Позиции карт в процентах (top%, left%)
    positions = [
        (5, 5),
        (5, 25),
        (5, 45),
        (5, 65),
        (5, 85)
    ]

    html_code = '''
    <div class="shadow-work" style="
        position: relative;
        width: 100%;
        max-width: 700px;
        aspect-ratio: 7/2;
        margin: 0 auto;
    ">
    '''

    for i, card in enumerate(cards_data):
        top_pct, left_pct = positions[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"

        html_code += f"""
        <div style="
            position:absolute;
            top:{top_pct}%;
            left:{left_pct}%;
            width:18%;
            aspect-ratio: 2/3;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{transform};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """

    html_code += '</div>'

    # Высота компонента Streamlit
    st.components.v1.html(html_code, height=200)

    return html_code

    
def render_single_card(cards):
    """
    cards — список из 1 карты с ключами: {'img': str, 'reversed': bool}
    """
    if len(cards) != 1:
        st.error("Single Card расклад принимает ровно одну карту!")
        return
    
    card = create_git_url_images(cards)[0]
    
    html_code = f"""
    <div style="display:flex; justify-content:center; margin-top:50px;">
        <div style="
            width:140px;
            height:220px;
            border-radius:10px;
            overflow:hidden;
            box-shadow:0 4px 8px rgba(0,0,0,0.25);
            transform:{'rotate(180deg)' if card['reversed'] else 'none'};
        ">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
    </div>
    """
    st.components.v1.html(html_code, height=300)
    
    return html_code
    
tarot_spreads = {
    "Single Card": render_single_card,          # 1 карта — быстрые инсайты
    "Three Card": render_three_card,            # 3 карты — Прошлое/Настоящее/Будущее
    "Celtic Cross": render_celtic_cross,        # 10 карт — комплексный анализ жизни
    "Horseshoe": render_horseshoe,              # 7 карт — ситуация + советы
    "Relationship Cross": render_relationship,  # 7 карт — анализ отношений
    "Career Path": render_career_path,          # 6 карт — профессиональное развитие
    "Decision Making": render_decision_making,  # 5 карт — выбор и руководство
    "Year Ahead": render_year_ahead,            # 13 карт — годовой прогноз
    "Spiritual Guidance": render_spiritual,     # 6 карт — духовное развитие
    "Chakra Alignment": render_chakra,          # 7 карт — баланс энергии
    "Shadow Work": render_shadow                # 5 карт — психологическая интеграция
}

def create_html_taro(cards, name):
    tarot_spreads[name](cards)