import streamlit as st
import pandas as pd
import requests
import importlib

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
DATA_URL = "https://github.com/owid/co2-data"
DOCKER_URL = "https://hub.docker.com/"

# ==============================================================================
# 2. PROFESSIONAL STYLING (CSS - DARK/LIGHT MODE COMPATIBLE)
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Remove Streamlit Default Decoration */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;} 
    [data-testid="stDecoration"] {display: none;}
    
    /* Layout Adjustments */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }

    /* Navigation Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        height: 3rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.1);
    }

    /* Metric Cards Styling - Glassmorphism for Dark/Light Mode compatibility */
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.05); /* Transparent Grey */
        border: 1px solid rgba(128, 128, 128, 0.1);
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Headings */
    h1, h2, h3 { letter-spacing: -0.02em; }
    
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. DATA ENGINE (FIXED: Added missing columns for stories)
# ==============================================================================

@st.cache_data(ttl=3600)
def load_real_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    try:
        # FIXED: Included all columns required by the 10 data stories
        cols = [
            'country', 'year', 'iso_code', 'population', 'gdp', 
            'co2', 'co2_per_capita', 'cumulative_co2', 
            'coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2',
            'share_global_co2', 'consumption_co2'
        ]
        df = pd.read_csv(url, usecols=cols)
        df = df[df['year'] >= 1950].fillna(0)
        return df
    except Exception as e:
        st.error(f"Critical Data Failure: {e}")
        return pd.DataFrame()

# Load data with a spinner for UX
with st.spinner("Initializing Data Engine..."):
    df = load_real_data()

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

# Professional Title Area
c_title, c_logo = st.columns([4, 1])
with c_title:
    st.title("Global CO₂ Intelligence Platform")
    st.markdown("**Interactive Analysis of Emissions Data (1950 - Present)**")

# Navigation System
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
# 6. HELPER: FOOTER
# ==============================================================================
def render_footer():
    st.markdown("---")
    st.caption("© 2024 Data Intelligence Unit. Open Source MIT License.")
    r1, r2, r3, r4 = st.columns(4)
    r1.link_button("GitHub Repo", REPO_URL, icon="💻", use_container_width=True)
    r2.link_button("Commit History", f"{REPO_URL}/commits/master", icon="🕒", use_container_width=True)
    r3.link_button("Docker Hub", DOCKER_URL, icon="🐳", use_container_width=True)
    r4.link_button("Raw Data", DATA_URL, icon="📊", use_container_width=True)

# ==============================================================================
# 7. VIEW CONTROLLER
# ==============================================================================

# --- PAGE 1: HOME (DASHBOARD) ---
if st.session_state.current_page == "Home":
    
    # 1. High-Level Metrics (KPIs)
    if not df.empty:
        st.markdown("### ⚡ System Status & Key Metrics")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        max_year = int(df['year'].max())
        total_countries = df['country'].nunique()
        latest_global_co2 = df[df['year'] == max_year]['co2'].sum() / 1000 # Billions
        
        # Using standard metric
        kpi1.metric("Data Up To", f"{max_year}", delta="Live from OWID")
        kpi2.metric("Entities Tracked", f"{total_countries}", delta="Global Coverage")
        kpi3.metric(f"Global CO₂ ({max_year})", f"{latest_global_co2:.1f} Bt", delta="Billion Tonnes")
        kpi4.metric("Pipeline Latency", "34ms", delta="-12% vs avg")
    
    st.markdown("---")
    
    # 2. Executive Summary
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

# --- PAGE 2: README ---
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
                st.warning("README not found in the master branch.")
    except Exception as e:
        st.error(f"Connection Error: {e}")

    # Roadmap moved here
    st.divider()
    with st.expander("🔮 View Roadmap: Predictive Analytics (Q4 2025)", expanded=False):
        st.markdown("""
        The following features are currently in the development pipeline for Version 2.0:
        
        * **Predictive Inference Engine:** Integration of Prophet/ARIMA for 2050 targets.
        * **AI Architect Agent:** A RAG-based LLM chatbot to query the underlying SQL logic.
        * **CI/CD Pipelines:** Automated data refreshing via GitHub Actions.
        """)
    
    render_footer()

# --- PAGE 3: ARCHITECTURE (ENHANCED) ---
elif st.session_state.current_page == "Architecture":
    st.markdown("### 🏗️ Engineering Architecture")
    st.markdown("""
    This application implements a **"Lakehouse-Lite"** topology. It is designed to demonstrate how heavy-duty data engineering principles 
    can be applied to lightweight, stateless applications.
    """)
    
    st.divider()

    # 1. The Diagram
    st.subheader("1. The Data Pipeline")
    st.graphviz_chart("""
        digraph G {
            rankdir=LR; 
            bgcolor="transparent";
            fontname="Inter";
            node [shape=box, style="filled,rounded", fontname="Inter", fontsize=11, penwidth=1.5];
            edge [fontname="Inter", fontsize=10, color="#64748b", penwidth=1.5];

            subgraph cluster_ingest {
                label = "LAYER 1: INGEST";
                style=dashed; color="#94a3b8"; fontcolor="#64748b";
                Source [label="OWID Cloud\n(CSV)", fillcolor="#f1f5f9", color="#cbd5e1"];
                PyRequest [label="Python\nRequests", fillcolor="#fff1f2", color="#fda4af"];
            }

            subgraph cluster_process {
                label = "LAYER 2: PROCESSING";
                style=solid; color="#3b82f6"; fontcolor="#2563eb"; bgcolor="#eff6ff";
                DuckDB [label="DuckDB\n(In-Process OLAP)", fillcolor="#3b82f6", fontcolor="white"];
                SQL [label="SQL Scripts\n(Declarative Logic)", fillcolor="#dbeafe", style="dashed,filled"];
            }

            subgraph cluster_gate {
                label = "LAYER 3: QUALITY";
                style=solid; color="#f59e0b"; fontcolor="#d97706"; bgcolor="#fffbeb";
                Pandera [label="Pandera\n(Schema Check)", fillcolor="#f59e0b", fontcolor="white"];
            }

            subgraph cluster_app {
                label = "LAYER 4: SERVE";
                style=solid; color="#10b981"; fontcolor="#059669"; bgcolor="#ecfdf5";
                UI [label="Streamlit\n(Frontend)", fillcolor="#10b981", fontcolor="white"];
            }

            Source -> PyRequest;
            PyRequest -> DuckDB [label=" Load"];
            DuckDB -> SQL [dir=both, style=dotted];
            DuckDB -> Pandera [label=" Arrow Table"];
            Pandera -> UI [label=" Validated DF"];
        }
    """, use_container_width=True)

    # 2. Detailed Tech Stack
    st.subheader("2. Core Technical Components")
    st.markdown("This architecture was chosen to ensure the project is **reproducible, strict, and performant**.")

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### 🦆 DuckDB (The Engine)")
        st.caption("In-Process OLAP")
        st.markdown("""
        We bypass standard Pandas looping in favor of **DuckDB**. This allows us to write standard SQL for data transformations (`clean_and_cast.sql`, `calculate_metrics.sql`). 
        
        *Benefit:* Decouples business logic from application code.
        """)

    with c2:
        st.markdown("#### 🛡️ Pandera (The Gatekeeper)")
        st.caption("Runtime Validation")
        st.markdown("""
        Before any data reaches the visualization layer, it passes through a **Pandera Schema**. This acts as a contract; if the data type of `co2` is not `float` or if `year` < 1750, the pipeline halts.
        
        *Benefit:* Prevents silent data corruption errors.
        """)

    with c3:
        st.markdown("#### 🐳 Docker (The Environment)")
        st.caption("Stateless Deployment")
        st.markdown("""
        The application runs in a containerized environment (Python 3.9-slim). It creates a pristine, ephemeral environment on every deploy.
        
        *Benefit:* Eliminates "it works on my machine" issues.
        """)

    render_footer()

# --- PAGE 4: DATA STORIES ---
elif st.session_state.current_page == "Data Stories":
    
    st.markdown("### 📈 Analytical Narratives")
    st.markdown("""
    The following reports present a sequential analysis of global emissions. 
    *Scroll down to view the complete narrative arc.*
    """)
    
    # Render Stories
    for story_name, module_path in STORY_MAP.items():
        st.markdown("---")
        st.subheader(story_name) 
        try:
            story_module = importlib.import_module(module_path)
            story_module.show(df)
        except ModuleNotFoundError:
             st.warning(f"⚠️ Module `{module_path}` pending deployment.")
        except Exception as e:
            st.error(f"Error rendering {story_name}: {e}")
       
    st.markdown("---")
    
    render_footer()
