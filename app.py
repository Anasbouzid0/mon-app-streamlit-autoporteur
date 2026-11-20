"""
Lanceur Streamlit Plein Écran pour les simulations de Physique-Chimie.
Permet d'afficher en plein écran (100vw x 100vh) toutes les simulations HTML
présentes dans le même dossier (ex. : 1BAC Théorème de l'énergie cinétique
et TC Leçon 3 : Le mouvement).

Exécution :
    streamlit run app.py
"""

from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components


# ==============================================================================
# 1. CONFIGURATION DE LA PAGE STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Simulations Physique-Chimie — Prof. BOUZID Anas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==============================================================================
# 2. CSS PLEIN ÉCRAN (SANS MARGES, SANS BARRES DE DÉFILEMENT, MULTI-VERSIONS)
# ==============================================================================
FULLSCREEN_CSS = """
<style>
    /* Supprime tout débordement et marges sur la fenêtre principale */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main {
        margin: 0 !important;
        padding: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        overflow: hidden !important;
        background-color: #f8fafc !important;
    }

    /* Supprime les espacements du conteneur de blocs Streamlit */
    .block-container,
    [data-testid="stMainBlockContainer"],
    .stAppViewBlockContainer {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
        width: 100vw !important;
        height: 100vh !important;
    }

    /* Masque le menu, la barre d'outils, le pied de page et la ligne décorative */
    #MainMenu,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Rend l'en-tête transparent sans bloquer les clics sur la simulation */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        overflow: visible !important;
        pointer-events: none !important;
        z-index: 999998 !important;
    }

    /* Garde le bouton d'ouverture de la barre latérale cliquable et discret */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stExpandSidebarButton"] {
        pointer-events: auto !important;
        position: fixed !important;
        bottom: 12px !important;
        left: 12px !important;
        top: auto !important;
        z-index: 999999 !important;
        background: rgba(41, 74, 107, 0.90) !important;
        color: #ffffff !important;
        border: 1.5px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 999px !important;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.25) !important;
    }

    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stExpandSidebarButton"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    /* S'assure que la barre latérale passe toujours au-dessus de l'iframe */
    section[data-testid="stSidebar"] {
        z-index: 999999 !important;
    }

    /* Force l'iframe de la simulation en véritable plein écran bord à bord */
    iframe,
    [data-testid="stIFrame"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        min-height: 100vh !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 1 !important;
    }
</style>
"""
st.markdown(FULLSCREEN_CSS, unsafe_allow_html=True)


# ==============================================================================
# 3. DÉTECTION AUTOMATIQUE DES SIMULATIONS HTML DANS LE DOSSIER
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent

# Libellés lisibles pour les fichiers connus du dossier
KNOWN_LABELS = {
    "simulation_autoporteur.html": "1BAC — Théorème de l'énergie cinétique",
    "simulation_mouvement_tc.html": "TC — Leçon 3 : Le mouvement",
    "simulation_autoporteur1.html": "TC — Leçon 3 : Le mouvement (autoporteur1)",
}


def discover_simulations(folder: Path) -> list[Path]:
    """Retourne la liste triée de tous les fichiers HTML du dossier."""
    return sorted(folder.glob("*.html"), key=lambda p: p.name.lower())


def get_display_name(file_path: Path) -> str:
    """Retourne un titre pédagogique propre pour un fichier HTML donné."""
    return KNOWN_LABELS.get(file_path.name, file_path.stem.replace("_", " ").title())


# ==============================================================================
# 4. SÉLECTION ET AFFICHAGE PLEIN ÉCRAN DE LA SIMULATION
# ==============================================================================
html_files = discover_simulations(BASE_DIR)

if not html_files:
    st.error(
        f"Aucun fichier HTML de simulation n'a été trouvé dans le dossier : `{BASE_DIR}`.\n\n"
        "Placez `simulation_autoporteur.html` et/ou `simulation_mouvement_tc.html` "
        "dans le même dossier que `app.py`."
    )
    st.stop()

# Menu latéral repliable pour changer de simulation sans encombrer l'écran
with st.sidebar:
    st.markdown("### 🧪 Simulations disponibles")
    labels = [get_display_name(f) for f in html_files]
    selected_label = st.radio(
        "Choisir une simulation :",
        options=labels,
        index=0,
    )
    selected_path = html_files[labels.index(selected_label)]

    st.divider()
    st.caption(
        "💡 **Astuce projection :** appuyez sur **F11** (Windows) ou "
        "**Ctrl + Cmd + F** (Mac) pour masquer la barre du navigateur et "
        "projeter en plein écran total."
    )

# Lecture sécurisée et injection en plein écran
try:
    html_content = selected_path.read_text(encoding="utf-8")
    # scrolling=False évite les doubles barres de défilement ; le CSS force 100vw x 100vh
    components.html(html_content, height=900, scrolling=False)
except Exception as exc:
    st.error(f"Erreur lors du chargement de `{selected_path.name}` : {exc}")
