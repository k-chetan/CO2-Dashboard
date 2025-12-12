import streamlit as st
import pandas as pd
import duckdb
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

# Constants
REPO_URL = "https://github.com/k-chetan/CO2-Dashboard" # Replace with your username
README_URL = "https://raw.githubusercontent.com/k-chetan/CO2-Dashboard/master/README.md"
DOCKER_URL = "https://hub.docker.com/r/kchetan/co2-dashboard"
# Live Stream URL (Raw CSV)
LIVE_DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
# Attribution URL (Main Repo with License)
OWID_REPO_URL = "https://github.com/owid/co2-data"

# ==============================================================================
# 2. STYLING (CSS)
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

    /* --- FOOTER BUTTONS --- */
    a[href="{REPO_URL}"], 
    a[href="{REPO_URL}/commits/master"], 
    a[href="{DOCKER_URL}"], 
    a[href="{OWID_REPO_URL}"] {{
        background-color: #ef4444 !important;
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

    a[href="{REPO_URL}"]:hover, 
    a[href="{REPO_URL}/commits/master"]:hover, 
    a[href="{DOCKER_URL}"]:hover, 
    a[href="{OWID_REPO_URL}"]:hover {{
        background-color: #22c55e !important;
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
# 3. LIVE DATA ENGINE (DEPENDENCY INJECTION)
# ==============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_live_data():
    """
    1. Fetches live raw data from GitHub (Extraction).
    2. Injects it into DuckDB as 'source_data' (Dependency Injection).
    3. Applies pure SQL logic from src/sql/ (Transformation).
    """
    try:
        # A. EXTRACT (Live Stream)
        # We read directly from the URL into a Pandas DataFrame (In-Memory)
        raw_df = pd.read_csv(LIVE_DATA_URL)
        
        # B. INITIALIZE ENGINE
        con = duckdb.connect(database=":memory:")
        
        # --- DE PRINCIPLE: DEPENDENCY INJECTION ---
        # We "inject" the live dataframe as the view 'source_data'.
        # The SQL script sees the exact same table name as it does in local dev.
        con.register('source_data', raw_df)
        
        # C. TRANSFORM (Reuse identical SQL logic)
        sql_dir = Path("src/sql")
        
        # 1. Clean & Cast (Requires 'source_data' view to exist)
        with open(sql_dir / "01_clean_and_cast.sql", "r") as f:
            con.execute("CREATE OR REPLACE VIEW cleaned_data AS " + f.read())

        # 2. Calculate Metrics
        with open(sql_dir / "02_calculate_metrics.sql", "r") as f:
            con.execute("CREATE OR REPLACE VIEW metrics_data AS " + f.read())

        # 3. Rolling Averages
        with open(sql_dir / "03_add_rolling_averages.sql", "r") as f:
            con.execute("CREATE OR REPLACE TABLE final_data AS " + f.read())
            
        # D. LOAD
        df_result = con.execute("SELECT * FROM final_data").fetchdf()
        con.close()
        
        return df_result

    except Exception as e:
        st.error(f"⚠️ Live Stream Failure: {e}")
        return pd.DataFrame()

# Execution with Feedback
status_box = st.empty()
if 'data_loaded' not in st.session_state:
    with status_box.container():
        st.info(f"📡 Establishing Uplink to Live Data Stream...")
        df = load_live_data()
        if not df.empty:
            st.success("✅ Live Data Acquired & Processed.")
            st.session_state.data_loaded = True
        status_box.empty()
else:
    df = load_live_data()

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
    st.markdown("**Live Streaming Analysis (Source: OWID GitHub)**")

st.markdown("<br>", unsafe_allow_html=True)

# UPDATED: 3 Columns instead of 4 (Removed Architecture)
nav_1, nav_2, nav_3 = st.columns(3)

def nav_button(label, col):
    is_active = st.session_state.current_page == label
    with col:
        if st.button(label, type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.current_page = label
            st.rerun()

nav_button("Home", nav_1)
nav_button("Project README", nav_2)
nav_button("Data Stories", nav_3)

st.markdown("---")

# ==============================================================================
# 6. HELPER: FOOTER (Minimalist & Compliant)
# ==============================================================================
def render_footer():
    st.markdown("---")
    # No text caption here. Just functional buttons.
    
    r1, r2, r3, r4 = st.columns(4)
    
    r1.link_button("GitHub Repo", REPO_URL, icon="💻", use_container_width=True)
    r2.link_button("Commit History", f"{REPO_URL}/commits/master", icon="🕒", use_container_width=True)
    r3.link_button("Docker Hub", DOCKER_URL, icon="🐳", use_container_width=True)
    # Attribution Button: Links to Main Repo (Contains License/Credits)
    r4.link_button("Data (OWID)", OWID_REPO_URL, icon="📊", use_container_width=True)

# ==============================================================================
# 7. VIEW CONTROLLER
# ==============================================================================

if st.session_state.current_page == "Home":
    if not df.empty:
        st.markdown("### ⚡ Live System Metrics")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        max_year = int(df['year'].max())
        total_countries = df['country'].nunique()
        latest_global_co2 = df[(df['year'] == max_year) & (df['country'] == 'World')]['co2'].sum() / 1000
        
        kpi1.metric("Data Up To", f"{max_year}", delta="Real-time Stream")
        kpi2.metric("Entities Tracked", f"{total_countries}", delta="Global Coverage")
        kpi3.metric(f"Global CO₂ ({max_year})", f"{latest_global_co2:.1f} Bt", delta="Billion Tonnes")
        kpi4.metric("Architecture", "Serverless", delta="In-Memory OLAP")
    
    st.markdown("---")
    st.markdown("### 📋 Executive Summary")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("""
        **Context:** This application operates on a **Live Streaming Architecture**. 
        Instead of reading static files, it pulls the latest raw dataset directly from the 
        [OWID GitHub Repository](https://github.com/owid/co2-data) every time the cache expires.
        
        **Engineering Highlights:**
        * **Dependency Injection:** The Pipeline is agnostic to the data source (File vs URL).
        * **Zero-Storage:** No persistence layer required; data lives in RAM.
        * **Declarative Transforms:** SQL logic is reused 100% from the local environment.
        """)
        
    with c2:
        st.info("💡 **Tip:** Navigate to the 'Data Stories' tab for deep-dive visualizations.")

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