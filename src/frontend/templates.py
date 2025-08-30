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

    # исходные позиции
    positions = [
        (220, 300), (220, 300), (400, 300), (40, 300),
        (220, 180), (220, 420), (40, 550), (120, 550),
        (200, 550), (280, 550)
    ]
    
    # сдвиг всех карт влево на 100px
    dx = 100
    positions = [(top, left - dx) for top, left in positions]

    html_code = '<div class="celtic-cross" style="position:relative; width:800px; height:600px;">'
    for i, card in enumerate(cards_data):
        top, left = positions[i]
        transform = "rotate(90deg)" if i == 1 else ("rotate(180deg)" if card["reversed"] else "none")
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

    st.components.v1.html(html_code, height=650)
    
    return html_code
    
def render_three_card(cards):
    """
    cards: список из 3 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)
    positions = [(200, 100), (200, 250), (200, 400)]  # top, left для каждой карты

    html_code = '<div class="three-card" style="position:relative; width:600px; height:400px;">'
    for i, card in enumerate(cards_data):
        top, left = positions[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"
        html_code += f"""
        <div style="position:absolute; top:{top}px; left:{left}px; width:120px; height:180px; border-radius:10px; overflow:hidden; box-shadow:0 4px 8px rgba(0,0,0,0.25); transform:{transform};">
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:contain;">
        </div>
        """
    html_code += '</div>'
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

    # Позиции карт (x, y)
    positions = [
        (100, 50),   # 1: партнер
        (300, 50),   # 2: себя
        (200, 150),  # 3: сила отношений (центр)
        (200, 250),  # 4: проблемы
        (100, 350),  # 5: совет
        (300, 350),  # 6: внешние влияния
        (200, 450),  # 7: итог
    ]

    html_code = '<div class="relationship-cross" style="position:relative; width:400px; height:500px;">'

    for i, card in enumerate(cards_data):
        top, left = positions[i]
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
    st.components.v1.html(html_code, height=500)
    
    return html_code

def render_career_path(cards):
    """
    cards: список из 6 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)

    # Позиции карт (x, y)
    positions = [
        (50, 50),   # 1: текущая ситуация
        (200, 50),  # 2: сильные стороны
        (350, 50),  # 3: слабые стороны
        (50, 280),  # 4: совет (чуть ниже, чтобы было больше места)
        (200, 280), # 5: внешние влияния
        (350, 280), # 6: результат
    ]

    html_code = '<div class="career-path" style="position:relative; width:520px; height:520px;">'

    for i, card in enumerate(cards_data):
        left, top = positions[i]  # исправил порядок, иначе путаница
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
            <img src="{card['img']}" style="width:100%; height:100%; object-fit:cover;">
        </div>
        """

    html_code += '</div>'

    st.components.v1.html(html_code, height=550)
    
    return html_code



def render_decision_making(cards):
    """
    cards: список из 5 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)

    # Позиции карт (top, left)
    positions = [
        (100, 50),   # 1: Вариант A
        (100, 200),  # 2: Вариант B
        (300, 50),   # 3: Преимущества/риски
        (300, 200),  # 4: Совет
        (500, 125),  # 5: Итог/решение
    ]

    html_code = '<div class="decision-making" style="position:relative; width:650px; height:450px;">'

    for i, card in enumerate(cards_data):
        top, left = positions[i]
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
    st.components.v1.html(html_code, height=450)
    
    return html_code
    

def render_year_ahead(cards):
    """
    cards: список из 13 карт, каждая {"name": str, "reversed": bool}
    """
    cards_data = create_git_url_images(cards)

    html_code = '<div class="year-ahead" style="position:relative; width:1400px; height:300px;">'

    # карты месяцев
    for i in range(12):
        top = 100
        left = 50 + i * 110
        card = cards_data[i]
        transform = "rotate(180deg)" if card["reversed"] else "none"
        html_code += f"""
        <div style="
            position:absolute;
            top:{top}px;
            left:{left}px;
            width:100px;
            height:160px;
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
    top = 10
    left = 600
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


def render_spiritual(cards):
    """
    cards: список из 6 карт, каждая {"name": str, "reversed": bool}
    """
    if len(cards) != 6:
        st.error("Необходимо ровно 6 карт")
        return

    cards_data = create_git_url_images(cards)

    html_code = '<div class="spiritual-guidance" style="position:relative; width:700px; height:350px;">'

    positions = [
        (50, 50), (50, 250), (50, 450),  # верхний ряд
        (200, 50), (200, 250), (200, 450) # нижний ряд
    ]

    for i, card in enumerate(cards_data):
        top, left = positions[i]
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

    html_code = '<div class="chakra-alignment" style="position:relative; width:180px; height:900px;">'

    # вертикальные позиции для 7 чакр
    positions = [
        (0, 30),    # Корневая
        (130, 30),  # Сакральная
        (260, 30),  # Солнечное сплетение
        (390, 30),  # Сердечная
        (520, 30),  # Горловая
        (650, 30),  # Третий глаз
        (780, 30),  # Коронная
    ]

    for i, card in enumerate(cards_data):
        top, left = positions[i]
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

    html_code = '<div class="shadow-work" style="position:relative; width:700px; height:200px;">'

    # горизонтальные позиции для 5 карт
    positions = [
        (10, 20),
        (10, 160),
        (10, 300),
        (10, 440),
        (10, 580)
    ]

    for i, card in enumerate(cards_data):
        top, left = positions[i]
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