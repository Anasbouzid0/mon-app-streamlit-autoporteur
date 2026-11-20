from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TP Physique 1BAC — Table à coussin d'air",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Suppression des marges et de l'en-tête Streamlit pour un affichage plein écran
st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

html_path = Path(__file__).parent / "simulation_autoporteur.html"
html_path = Path(__file__).parent / "simulation_autoporteur1.html"

if html_path.exists():
  html_content = html_path.read_text(encoding="utf-8")
  components.html(html_content, height=1000, scrolling=True)
else:
  st.error("Fichier 'simulation_autoporteur.html' introuvable.")
