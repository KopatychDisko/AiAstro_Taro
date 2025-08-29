import streamlit as st
from pathlib import Path

# путь к SVG
svg_path = Path("C:\\Users\\kopatych\\Kanye - Natal Chart.svg")

with open(svg_path, "r", encoding="utf-8") as f:
    svg_content = f.read()

# вставляем SVG прямо в Streamlit через HTML
st.components.v1.html(svg_content, height=500)
  # возвращаем указатель в начало
