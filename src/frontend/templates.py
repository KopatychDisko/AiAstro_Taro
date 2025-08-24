import streamlit as st

def create_git_url_images(tarot_photo: list):
    photos_urls = []
    for info in tarot_photo:
        name, reversed = info['name'], info['reversed']
        tarot_url = f'https://github.com/KopatychDisko/tarot_images/blob/main/images/{name}.jpeg?raw=true'
        photos_urls.append({"img": tarot_url, "reversed": reversed})
    return photos_urls

def card_html(card, extra_class=""):
    transform = "rotate(180deg)" if card['reversed'] else "none"
    return f"""
    <div class="card {extra_class}" style="transform:{transform};">
      <img src="{card['img']}">
    </div>
    """

import streamlit as st

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