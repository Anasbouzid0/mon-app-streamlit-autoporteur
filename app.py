"""
Lanceur Streamlit Plein Écran pour les simulations de Physique-Chimie.
Compatible local (streamlit run app.py) et Streamlit Community Cloud.

Fichiers attendus dans le même dossier que app.py :
    - simulation_autoporteur.html   (1BAC — Théorème de l'énergie cinétique)
    - simulation_autoporteur1.html  (TC — Leçon 3 : Le mouvement)
"""

from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components


# ==============================================================================
# 1. CONFIGURATION DE LA PAGE
# ==============================================================================
st.set_page_config(
    page_title="Simulations Physique-Chimie — Prof. BOUZID Anas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==============================================================================
# 2. CSS PLEIN ÉCRAN FIABLE (SANS POSITION:FIXED QUI MASQUE L'IFRAME)
# ==============================================================================
st.markdown(
    """
    <style>
        /* Masque les éléments par défaut de Streamlit */
        #MainMenu,
        footer,
        header[data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
        }

        /* Supprime les grandes marges de la page */
        .block-container,
        [data-testid="stMainBlockContainer"] {
            padding: 0.35rem 0.5rem 0 0.5rem !important;
            max-width: 100% !important;
        }

        /* Réduit l'espace vertical entre la barre du haut et la simulation */
        [data-testid="stVerticalBlock"] {
            gap: 0.35rem !important;
        }

        /* Style compact des boutons de sélection en haut */
        .stButton > button {
            padding: 0.25rem 0.75rem !important;
            min-height: 34px !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }

        /* Affiche l'iframe sur toute la largeur et toute la hauteur restante */
        iframe {
            width: 100% !important;
            height: calc(100vh - 52px) !important;
            min-height: 560px !important;
            border: none !important;
            display: block !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 3. DÉTECTION DES FICHIERS HTML DANS LE DOSSIER
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent

KNOWN_LABELS = {
    "simulation_autoporteur.html": "1BAC — Théorème de l'énergie cinétique",
    "simulation_autoporteur1.html": "TC — Leçon 3 : Le mouvement",
    "simulation_mouvement_tc.html": "TC — Leçon 3 : Le mouvement",
}


def discover_simulations(folder: Path) -> list[Path]:
    """Retourne tous les fichiers .html du dossier, triés par nom."""
    return sorted(folder.glob("*.html"), key=lambda p: p.name.lower())


def get_label(path: Path) -> str:
    """Retourne un libellé lisible pour le bouton de sélection."""
    return KNOWN_LABELS.get(path.name, path.stem.replace("_", " ").title())


def load_html_safely(path: Path) -> str:
    """Lit un fichier HTML et nettoie d'éventuelles balises Markdown ```html."""
    content = path.read_text(encoding="utf-8", errors="replace").strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines).strip()
    return content


# ==============================================================================
# 4. BARRE DE SÉLECTION COMPACTE EN HAUT + AFFICHAGE DE LA SIMULATION
# ==============================================================================
html_files = discover_simulations(BASE_DIR)

if not html_files:
    st.error(
        f"Aucun fichier `.html` trouvé dans `{BASE_DIR}`. "
        "Vérifiez que `simulation_autoporteur.html` et `simulation_autoporteur1.html` "
        "sont bien dans le même dossier que `app.py`."
    )
    st.stop()

# Mémorise la simulation active dans la session
if "active_sim" not in st.session_state or st.session_state.active_sim not in [f.name for f in html_files]:
    st.session_state.active_sim = html_files[0].name

# Barre supérieure compacte (1 bouton par simulation + rappel F11)
cols = st.columns([3] * len(html_files) + [2], vertical_alignment="center")
for idx, file_path in enumerate(html_files):
    is_active = st.session_state.active_sim == file_path.name
    with cols[idx]:
        if st.button(
            get_label(file_path),
            key=f"btn_{file_path.name}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.active_sim = file_path.name
            st.rerun()

with cols[-1]:
    st.markdown(
        "<div style='text-align:right; font-size:0.78rem; color:#475569; padding-right:4px;'>"
        "<b>F11</b> : plein écran PC"
        "</div>",
        unsafe_allow_html=True,
    )

# Chargement et rendu de la simulation sélectionnée
selected_path = next(f for f in html_files if f.name == st.session_state.active_sim)

try:
    html_content = load_html_safely(selected_path)
    if not html_content:
        st.warning(f"Le fichier `{selected_path.name}` est vide.")
    else:
        components.html(html_content, height=850, scrolling=True)
except Exception as exc:
    st.error(f"Impossible de charger `{selected_path.name}` : {exc}")
