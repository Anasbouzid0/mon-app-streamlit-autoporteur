from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Simulation Autoporteur - Plan Incliné",
    layout="wide",
)

html_path = Path(__file__).parent / "simulation_autoporteur.html"

if html_path.exists():
  html_content = html_path.read_text(encoding="utf-8")
  components.html(html_content, height=920, scrolling=True)
else:
  st.error(
      "Fichier 'simulation_autoporteur.html' introuvable dans le dossier du"
      " script."
  )
