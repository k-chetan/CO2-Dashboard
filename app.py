import streamlit as st
import pandas as pd
import requests
import importlib
from pathlib import Path

# ==============================================================================
# 1. CONFIGURATION & STATE
# ==============================================================================

st.set_page_config(
    page_title="Global CO₂ Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Global Constants
REPO_URL = "https://github.com/k-chetan/CO2-Dashboard"
README_URL = "https://raw.githubusercontent.com/k-chetan/CO2-Dashboard/master/README.md"
DOCKER_URL = "https://hub.docker.com/r/kchetan/co2-dashboard"
RAW_DATA_URL = "https://github.com/owid/co2-data"
DATA_PATH = Path("data/processed/co2_data.parquet")

# ==============================================================================
# 2. PROFESSIONAL STYLING (CSS)
# ==============================================================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    
    /* Remove Decorations */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="stToolbar"] {{visibility: hidden;}} 
    [data-testid="stDecoration"] {{display: none;}}
    
    /* Layout */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }}

    /* --- NAVIGATION BUTTONS (Top) --- */
    div.stButton > button {{
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        height: 3rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: all 0.2s ease;
    }}
    div.stButton > button:hover {{
        border-color: #3b82f6;
        color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.1);
    }}

    /* --- FOOTER BUTTONS (Attention Seeking) --- */
    /* Target specific links by their HREF attribute to style only the footer buttons */
    
    a[href="{REPO_URL}"], 
    a[href="{REPO_URL}/commits/master"], 
    a[href="{DOCKER_URL}"], 
    a[href="{RAW_DATA_URL}"] {{
        background-color: #ef4444 !important; /* Red */
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        text-align: center !important;
        text-decoration: none !important;
        border-radius: 8px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 3rem !important;
        transition: background-color 0.3s ease, transform 0.2s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}

    /* Hover State: Turn Green */
    a[href="{REPO_URL}"]:hover, 
    a[href="{REPO_URL}/commits/master"]:hover, 
    a[href="{DOCKER_URL}"]:hover, 
    a[href="{RAW_DATA_URL}"]:hover {{
        background-color: #22c55e !important; /* Green */
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }}

    /* Metric Cards */
    [data-testid="stMetric"] {{
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
        padding: 15px;
        border-radius: 8px;
    }}
    
    h1, h2, h3 {{ letter-spacing: -0.02em; }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. DATA ENGINE
# ==============================================================================

@st.cache_data(ttl=3600)
def load_data():
    try:
        if not DATA_PATH.exists():
            st.error("⚠️ Data not found. Run 'make run-pipeline' or 'make docker-pipeline' first.")
            return pd.DataFrame()
        
        df = pd.read_parquet(DATA_PATH)
        return df
    except Exception as e:
        st.error(f"Critical Data Failure: {e}")
        return pd.DataFrame()

with st.spinner("Initializing Data Engine..."):
    df = load_data()

# ==============================================================================
# 4. STORY REGISTRY
# ==============================================================================

STORY_MAP = {
    "1. Historical Responsibility": "stories.story_01_Historical_Responsibility",
    "2. Personal Footprint": "stories.story_02_The_Personal_Footprint",
    "3. The Global Trend": "stories.story_03_The_Global_Trend",
    "4. Today's Heavy Hitters": "stories.story_04_Todays_Heavy_Hitters",
    "5. The Great Acceleration": "stories.story_05_The_Great_Acceleration",
    "6. The Fuel Mix": "stories.story_06_The_Fuel_Mix",
    "7. Volatility & Shocks": "stories.story_07_Volatility_and_Shocks",
    "8. The Hope Story": "stories.story_08_The_Hope_Story_Decoupling",
    "9. Consumption vs. Production": "stories.story_09_Consumption_vs_Production",
    "10. The Analyst's View": "stories.story_10_The_Analysts_View"
}

# ==============================================================================
# 5. HEADER & NAVIGATION
# ==============================================================================

c_title, c_logo = st.columns([4, 1])
with c_title:
    st.title("Global CO₂ Intelligence Platform")
    st.markdown("**Interactive Analysis of Emissions Data (1750 - Present)**")

st.markdown("<br>", unsafe_allow_html=True)
nav_1, nav_2, nav_3, nav_4 = st.columns(4)

def nav_button(label, col):
    is_active = st.session_state.current_page == label
    with col:
        if st.button(label, type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.current_page = label
            st.rerun()

nav_button("Home", nav_1)
nav_button("Project README", nav_2)
nav_button("Architecture", nav_3)
nav_button("Data Stories", nav_4)

st.markdown("---")

# ==============================================================================
# 6. HELPER: FOOTER (LINKS MUST MATCH CSS EXACTLY)
# ==============================================================================
def render_footer():
    st.markdown("---")
    st.caption("© 2024 Data Intelligence Unit. Open Source MIT License.")
    r1, r2, r3, r4 = st.columns(4)
    
    # These URLs are targeted by the CSS above to turn Red -> Green
    r1.link_button("GitHub Repo", REPO_URL, icon="💻", use_container_width=True)
    r2.link_button("Commit History", f"{REPO_URL}/commits/master", icon="🕒", use_container_width=True)
    r3.link_button("Docker Hub", DOCKER_URL, icon="🐳", use_container_width=True)
    r4.link_button("Raw Data", RAW_DATA_URL, icon="📊", use_container_width=True)

# ==============================================================================
# 7. VIEW CONTROLLER
# ==============================================================================

if st.session_state.current_page == "Home":
    if not df.empty:
        st.markdown("### ⚡ System Status & Key Metrics")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        max_year = int(df['year'].max())
        total_countries = df['country'].nunique()
        latest_global_co2 = df[(df['year'] == max_year) & (df['country'] == 'World')]['co2'].sum() / 1000
        
        kpi1.metric("Data Up To", f"{max_year}", delta="Live from Pipeline")
        kpi2.metric("Entities Tracked", f"{total_countries}", delta="Global Coverage")
        kpi3.metric(f"Global CO₂ ({max_year})", f"{latest_global_co2:.1f} Bt", delta="Billion Tonnes")
        kpi4.metric("Pipeline Status", "Ready", delta="Parquet Optimized")
    
    st.markdown("---")
    st.markdown("### 📋 Executive Summary")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("""
        **Context:** Climate change is the defining data challenge of our time. This application serves as a demonstration of rigorous **Data Engineering** principles applied to environmental science.
        
        **Engineering Highlights:**
        * **Declarative Transformations:** Logic resides in SQL/DuckDB, not opaque Python loops.
        * **Strict Schema Validation:** Incoming data is vetted by Pandera before rendering.
        * **Containerized Reproducibility:** The environment is strictly defined via Docker.
        """)
        
    with c2:
        st.info("💡 **Tip:** Navigate to the 'Data Stories' tab for deep-dive visualizations on specific emission drivers.")

    st.markdown("<br>", unsafe_allow_html=True)
    render_footer()

elif st.session_state.current_page == "Project README":
    st.markdown("### 📑 Project Documentation")
    st.caption(f"Fetched dynamically from: {REPO_URL}")
    st.divider()
    
    try:
        with st.spinner("Fetching documentation..."):
            response = requests.get(README_URL)
            if response.status_code == 200:
                st.markdown(response.text)
            else:
                st.warning(f"README not found at {README_URL}")
    except Exception as e:
        st.error(f"Connection Error: {e}")

    st.divider()
    with st.expander("🔮 View Roadmap: Predictive Analytics (Q4 2025)", expanded=False):
        st.markdown("""
        The following features are currently in the development pipeline for Version 2.0:
        * **Predictive Inference Engine:** Integration of Prophet/ARIMA for 2050 targets.
        * **AI Architect Agent:** A RAG-based LLM chatbot to query the underlying SQL logic.
        * **CI/CD Pipelines:** Automated data refreshing via GitHub Actions.
        """)
    
    render_footer()

elif st.session_state.current_page == "Architecture":
    st.markdown("### 🏗️ Engineering Architecture")
    st.markdown("""
    This application implements a **"Lakehouse-Lite"** topology. It is designed to demonstrate how heavy-duty data engineering principles 
    can be applied to lightweight, stateless applications.
    """)
    st.divider()

    st.subheader("1. The Data Pipeline")
    st.graphviz_chart("""
        digraph G {
            rankdir=LR; 
            bgcolor="transparent";
            node [shape=box, style="filled,rounded", fontname="Sans", fontsize=10];
            edge [fontname="Sans", fontsize=9, color="#64748b"];

            subgraph cluster_etl {
                label = "ETL Pipeline (Makefile)";
                style=dashed; color="#94a3b8";
                Ingest [label="Ingest (Python)", fillcolor="#f1f5f9"];
                DuckDB [label="DuckDB (SQL)", fillcolor="#3b82f6", fontcolor="white"];
                Validation [label="Pandera (Check)", fillcolor="#f59e0b", fontcolor="white"];
            }

            subgraph cluster_app {
                label = "Frontend";
                style=solid; color="#10b981";
                Streamlit [label="Streamlit App", fillcolor="#10b981", fontcolor="white"];
            }

            Ingest -> DuckDB [label=" Raw CSV"];
            DuckDB -> Validation [label=" Transform"];
            Validation -> Streamlit [label=" Parquet"];
        }
    """, use_container_width=True)

    st.subheader("2. Project Directory Structure")
    st.markdown("The codebase follows a strict separation of concerns, isolating logic (`src`), data (`data`), and presentation (`stories`).")
    
    st.code("""
.
├── .dockerignore              # [Infra] Excludes data/venv from build
├── .gitignore                 # [Infra] Excludes data/venv from git
├── docker-compose.yml         # [Infra] Volume mapping & service
├── Dockerfile                 # [Infra] Container blueprint
├── Makefile                   # [Auto]  Command shortcuts
├── README.md                  # [Docs]  Project documentation
├── requirements.txt           # [Deps]  Python dependencies
├── app.py                     # [Core]  Streamlit Frontend
│
├── data/                      # [Data]  (Local only, ignored by Git)
│   ├── raw/                   #         -> .gitkeep
│   └── processed/             #         -> .gitkeep
│
├── src/                       # [Logic]
│   ├── __init__.py
│   ├── ingest.py              #         -> Requests
│   ├── transform.py           #         -> DuckDB
│   ├── validation.py          #         -> Pandera Schema
│   │
│   ├── sql/                   # [SQL]
│   │   ├── 01_clean_and_cast.sql
│   │   ├── 02_calculate_metrics.sql
│   │   └── 03_add_rolling_averages.sql
│   │
│   └── tests/                 # [QA]
│       ├── __init__.py
│       └── test_pipeline.py   #         -> Pytest
│
└── stories/                   # [Viz]
    ├── __init__.py
    ├── story_01_Historical_Responsibility.py
    ├── ... (Stories 1-10)
    └── story_10_The_Analysts_View.py
    """, language="text")

    st.subheader("3. Core Technical Components")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🦆 DuckDB (The Engine)")
        st.caption("In-Process OLAP")
        st.markdown("Runs SQL transformations on raw CSVs without loading them entirely into memory.")
    with c2:
        st.markdown("#### 🛡️ Pandera (The Gatekeeper)")
        st.caption("Runtime Validation")
        st.markdown("Enforces a strict schema contract. If data violates the contract, the pipeline halts.")
    with c3:
        st.markdown("#### 🐳 Docker (The Environment)")
        st.caption("Stateless Deployment")
        st.markdown("Ensures the entire environment (OS + Python) is reproducible on any machine.")

    render_footer()

elif st.session_state.current_page == "Data Stories":
    st.markdown("### 📈 Analytical Narratives")
    for story_name, module_path in STORY_MAP.items():
        st.markdown("---")
        try:
            story_module = importlib.import_module(module_path)
            story_module.show(df)
        except ModuleNotFoundError:
             st.warning(f"⚠️ Module `{module_path}` pending deployment.")
        except Exception as e:
            st.error(f"Error rendering {story_name}: {e}")
    st.markdown("---")
    render_footer()
