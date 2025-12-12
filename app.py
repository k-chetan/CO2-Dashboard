import streamlit as st
import pandas as pd
import duckdb
import importlib
from pathlib import Path

# ==============================================================================
# 1. CONFIGURATION & STATE
# ==============================================================================

st.set_page_config(
    page_title="Global CO₂ Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Constants
REPO_URL = "https://github.com/k-chetan/CO2-Dashboard" 
README_URL = "https://github.com/k-chetan/CO2-Dashboard/blob/master/README.md"
DOCKER_URL = "https://hub.docker.com/r/kchetan/co2-dashboard"
LIVE_DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
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
    div.stButton > button, 
    a[href="{README_URL}"] {{
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        height: 3rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: inherit;
    }}
    
    div.stButton > button:hover, 
    a[href="{README_URL}"]:hover {{
        border-color: #3b82f6;
        color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.1);
    }}

    /* --- FOOTER BUTTONS --- */
    /* Target specific links by HREF to apply button styling */
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
    Fetches live raw data from the repository, injects it into DuckDB, 
    and applies SQL transformations in-memory.
    """
    try:
        # A. EXTRACT (Live Stream)
        raw_df = pd.read_csv(LIVE_DATA_URL)
        
        # B. INITIALIZE ENGINE
        con = duckdb.connect(database=":memory:")
        
        # Dependency Injection: Register the live dataframe as 'source_data'
        con.register('source_data', raw_df)
        
        # C. TRANSFORM
        sql_dir = Path("src/sql")
        
        # 1. Clean & Cast
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
        st.error(f"System Error (Data Pipeline): {e}")
        return pd.DataFrame()

# Execution
status_box = st.empty()
if 'data_loaded' not in st.session_state:
    with status_box.container():
        st.info("Initializing connection to live data stream...")
        df = load_live_data()
        if not df.empty:
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
    st.title("Global CO₂ Analysis Platform")
    st.markdown("**Live Data Stream (Source: OWID/Global Carbon Project)**")

st.markdown("<br>", unsafe_allow_html=True)

# Navigation: 3 Columns
nav_1, nav_2, nav_3 = st.columns(3)

def nav_button(label, col):
    is_active = st.session_state.current_page == label
    with col:
        if st.button(label, type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state.current_page = label
            st.rerun()

# Tab 1: Home
nav_button("Home", nav_1)

# Tab 2: Data Stories
nav_button("Data Stories", nav_2)

# Tab 3: Project Documentation (External Link)
with nav_3:
    st.link_button("Project Documentation ↗", README_URL, use_container_width=True)

st.markdown("---")

# ==============================================================================
# 6. FOOTER
# ==============================================================================
def render_footer():
    st.markdown("---")
    r1, r2, r3, r4 = st.columns(4)
    
    r1.link_button("GitHub Repo", REPO_URL, icon="💻", use_container_width=True)
    r2.link_button("Commit History", f"{REPO_URL}/commits/master", icon="🕒", use_container_width=True)
    r3.link_button("Docker Hub", DOCKER_URL, icon="🐳", use_container_width=True)
    r4.link_button("Data Source (OWID)", OWID_REPO_URL, icon="📊", use_container_width=True)

# ==============================================================================
# 7. VIEW CONTROLLER
# ==============================================================================

if st.session_state.current_page == "Home":
    if not df.empty:
        st.markdown("### System Status")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        max_year = int(df['year'].max())
        total_countries = df['country'].nunique()
        latest_global_co2 = df[(df['year'] == max_year) & (df['country'] == 'World')]['co2'].sum() / 1000
        
        # FIX: Replaced static "Architecture" text with dynamic "Total Records" count
        kpi1.metric("Data Year", f"{max_year}")
        kpi2.metric("Entities Tracked", f"{total_countries}")
        kpi3.metric(f"Global CO₂ ({max_year})", f"{latest_global_co2:.1f} Bt")
        kpi4.metric("Dataset Volume", f"{len(df):,}", delta="Rows Processed")
    
    st.markdown("---")
    st.markdown("### Project Overview")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("""
        **Objective:** This application provides an interactive analysis of global CO₂ emissions data from 1750 to the present.
        
        **Technical Architecture:**
        * **Live Streaming:** The application fetches the raw dataset directly from the source repository upon initialization.
        * **Source-Agnostic Pipeline:** Data transformation logic is decoupled from data extraction, enabling identical execution in local and cloud environments.
        * **Zero-Storage:** No persistent storage layer is used. All processing (Ingestion, Transformation, Validation) occurs in volatile memory using DuckDB.
        """)
        
    with c2:
        st.info("ℹ️ **Navigation:** Select 'Data Stories' to view specific analytical narratives.")

    st.markdown("<br>", unsafe_allow_html=True)
    render_footer()

elif st.session_state.current_page == "Data Stories":
    st.markdown("### Analytical Narratives")
    for story_name, module_path in STORY_MAP.items():
        st.markdown("---")
        try:
            story_module = importlib.import_module(module_path)
            story_module.show(df)
        except ModuleNotFoundError:
             st.warning(f"Module `{module_path}` not found.")
        except Exception as e:
            st.error(f"Error rendering {story_name}: {e}")
    st.markdown("---")
    render_footer()