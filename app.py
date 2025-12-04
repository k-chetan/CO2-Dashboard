import streamlit as st
import pandas as pd
import requests
import importlib

# ==============================================================================
# 1. CONFIGURATION & DESIGN SYSTEM
# ==============================================================================

st.set_page_config(
    page_title="Data Intensive Application",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded" # Force open by default
)

# Global Constants
REPO_URL = "https://github.com/k-chetan/CO2-Dashboard"
README_URL = "https://raw.githubusercontent.com/k-chetan/CO2-Dashboard/master/README.md"
DATA_URL = "https://github.com/owid/co2-data"

# ------------------------------------------------------------------------------
# 1.1 CSS ARCHITECTURE
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    :root { --primary-color: #10B981; }

    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 5rem;
        margin: auto;
    }

    /* --- SIDEBAR LOCK --- */
    /* 1. Hide the arrow at the top right of the sidebar (The 'Close' button) */
    [data-testid="stSidebar"] button[kind="header"] {
        display: none;
    }
    
    /* 2. Hide the arrow in the main app (The 'Open' button) */
    /* This ensures if it glitches closed, the arrow is gone, but we rely on initial_sidebar_state="expanded" */
    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }

    /* 3. Style the sidebar border */
    [data-testid="stSidebar"] { 
        border-right: 1px solid rgba(128,128,128,0.2); 
    }
    
    /* Card Styling */
    .story-card {
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        background-color: var(--secondary-background-color);
        transition: transform 0.2s;
    }
    .story-card:hover {
        transform: translateY(-2px);
        border-color: var(--primary-color);
    }

    h1, h2, h3 { font-weight: 700; letter-spacing: -0.025em; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DATA INGESTION
# ==============================================================================

@st.cache_data(ttl=3600)
def load_real_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    try:
        cols = ['country', 'year', 'iso_code', 'population', 'gdp', 'co2', 'co2_per_capita', 'cumulative_co2', 'coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'share_global_co2']
        df = pd.read_csv(url, usecols=cols)
        df = df[df['year'] >= 1950].fillna(0)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

df = load_real_data()

# ==============================================================================
# 3. STORY REGISTRY
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
# 4. SIDEBAR NAVIGATION
# ==============================================================================

# Initialize Session State for Navigation
if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "Home"

with st.sidebar:
    st.markdown("### Data Intensive Application")
    st.caption("Global CO2 Analysis")
    
    # NAVIGATION (Controlled by Session State)
    main_page = st.radio(
        "Navigation", 
        ["Home", "Project README", "Architecture", "Data Stories"], 
        label_visibility="collapsed",
        key="nav_selection" # Links this widget to session_state
    )
    
    st.markdown("---")
    
    # Level 2 Navigation (Only appears if Data Stories is selected)
    selected_story_module = None
    if main_page == "Data Stories":
        st.markdown("**Select Analysis:**")
        selected_story_name = st.radio(
            "Story",
            list(STORY_MAP.keys()),
            label_visibility="collapsed"
        )
        selected_story_module = STORY_MAP[selected_story_name]
    
    # Resources
    st.markdown("### Resources")
    st.link_button("GitHub Repository", REPO_URL, icon="💻")
    st.link_button("Commit History", f"{REPO_URL}/commits/master", icon="🕒")
    st.link_button("Raw Data Source", DATA_URL, icon="📊")

    st.divider()

    # Chat
    with st.popover("💬 Ask AI"):
        st.markdown("**AI Assistant**")
        if st.text_input("Ask about the pipeline...", placeholder="e.g. Normalization?"):
            st.info("System Notification: This conversational interface is scheduled for implementation in Phase 2.")

# ==============================================================================
# 5. PAGE ROUTING
# ==============================================================================

# --- PAGE 1: HOME ---
if main_page == "Home":
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Data Intensive Application")
    st.subheader("Global CO2 Analysis")
    
    st.image("https://images.unsplash.com/photo-1611273426728-79658f0ac959?q=80&w=2070&auto=format&fit=crop", 
             caption="Industrial emissions contributing to the global carbon budget.", 
             use_container_width=True)

    # CALL TO ACTION BUTTON
    # This button updates the session state to jump to the stories tab
    def go_to_stories():
        st.session_state.nav_selection = "Data Stories"

    st.button("🚀 Explore the Data Stories", on_click=go_to_stories, type="primary", use_container_width=True)

    st.markdown("---")

    c1, c2 = st.columns(2)
    c1.link_button("Source Code", REPO_URL, use_container_width=True)
    c2.link_button("Data Schema", "https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv", use_container_width=True)

    st.markdown("### Executive Summary")
    st.markdown("""
    Climate change is the defining data challenge of our time. This application is not merely a visualization tool, 
    but a demonstration of rigorous **Data Engineering** applied to environmental science.
    
    **Core Engineering Principles:**
    * **Reproducibility:** The entire pipeline is containerized, ensuring that results are consistent across any computing environment.
    * **Data Integrity:** We strictly enforce schema validation (via Pandera) to reject malformed data before it reaches the presentation layer.
    * **Performance:** By utilizing declarative SQL transformations (via DuckDB) rather than imperative Python loops, we achieve high-throughput data processing.
    """)

# --- PAGE 2: README ---
elif main_page == "Project README":
    st.title("Project Documentation")
    st.markdown("Live fetch from the GitHub Master Branch.")
    st.divider()
    try:
        response = requests.get(README_URL)
        if response.status_code == 200:
            st.markdown(response.text)
        else:
            st.warning("README not found in the master branch.")
    except:
        st.error("Could not fetch README.")

# --- PAGE 3: ARCHITECTURE ---
elif main_page == "Architecture":
    st.title("System Architecture")
    st.markdown("### Architectural Decisions")
    
    st.markdown("""
    The system uses a **"Lakehouse-Lite"** topology suitable for high-performance analytical apps.
    
    **Why SQL-First?**
    Data transformation logic is often buried in opaque Python scripts. By moving logic to **DuckDB** (an in-process OLAP database), 
    we make the transformations declarative, readable, and significantly faster due to DuckDB's columnar execution engine.
    
    **Why strict validation?**
    Garbage-in, garbage-out. The **Pandera** validation layer acts as a strict contract, ensuring that no visualization 
    renders misleading information due to upstream data errors.
    """)
    
    st.divider()
    
    st.graphviz_chart("""
        digraph G {
            rankdir=LR; 
            bgcolor="transparent";
            compound=true;
            fontname="Inter";
            node [shape=box, style="filled,rounded", fontname="Inter", fontsize=10, penwidth=0];
            edge [fontname="Inter", fontsize=9, color="#94a3b8"];

            subgraph cluster_raw {
                label = "LAYER 1: INGESTION";
                style=dashed; color="#94a3b8"; fontcolor="#94a3b8";
                Source [label="☁️ OWID Data\n(GitHub RAW)", fillcolor="#f1f5f9", fontcolor="#475569"];
                Ingest [label="🐍 Ingest Script\n(Pandas/Requests)", fillcolor="#e2e8f0", fontcolor="#1e293b"];
            }

            subgraph cluster_engine {
                label = "LAYER 2: DECLARATIVE ENGINE";
                style=solid; color="#10b981"; fontcolor="#10b981"; bgcolor="#ecfdf5";
                DuckDB [label="🦆 DuckDB\n(In-Memory OLAP)", fillcolor="#10b981", fontcolor="white", shape=cylinder];
                SQL [label="📜 SQL Scripts\n(Transformations)", fillcolor="#d1fae5", fontcolor="#065f46"];
                DuckDB -> SQL [dir=none, style=dotted];
            }

            subgraph cluster_quality {
                label = "LAYER 3: QUALITY GATE";
                style=dashed; color="#f59e0b"; fontcolor="#f59e0b";
                Pandera [label="🛡️ Pandera\n(Schema Validation)", fillcolor="#fef3c7", fontcolor="#92400e"];
            }

            subgraph cluster_app {
                label = "LAYER 4: INTELLIGENT APP";
                style=solid; color="#3b82f6"; fontcolor="#3b82f6";
                Streamlit [label="📊 Streamlit UI\n(The Dashboard)", fillcolor="#3b82f6", fontcolor="white"];
                ML [label="🤖 ML Forecasting\n(Prophet/ARIMA)\n[Future Q4]", fillcolor="#f1f5f9", fontcolor="#64748b", style="dashed,rounded"];
                LLM [label="💬 AI Architect\n(RAG/Gemini)\n[Future Q4]", fillcolor="#f1f5f9", fontcolor="#64748b", style="dashed,rounded"];
            }

            Source -> Ingest;
            Ingest -> DuckDB [label=" Load Raw"];
            DuckDB -> Pandera [label=" Output DF"];
            Pandera -> Streamlit [label=" Verified Data"];
            DuckDB -> ML [style=dashed, color="#cbd5e1", constraint=false];
            ML -> Streamlit [style=dashed, color="#cbd5e1", label=" Predictions"];
            Streamlit -> LLM [style=dashed, dir=both, color="#cbd5e1", label=" Query"];
        }
    """)

# --- PAGE 4: DATA STORIES (SIDEBAR CONTROLLED) ---
elif main_page == "Data Stories":
    if selected_story_module:
        try:
            # Dynamic Import
            story_module = importlib.import_module(selected_story_module)
            # Execute
            story_module.show(df)
        except ModuleNotFoundError:
            st.error(f"⚠️ Error: The file `{selected_story_module}.py` was not found in the 'stories' folder.")
            st.markdown("Did you run the file renaming commands in the terminal?")
        except AttributeError:
            st.error(f"⚠️ Error: The file `{selected_story_module}.py` is missing the `show(df)` function.")
    else:
        st.info("Select a story from the sidebar to begin analysis.")

    # Footer Guardrail
    st.markdown("---")
    st.markdown("### Predictive Analytics")
    if st.button("Run Predictive ML Model (v2.0)", type="primary"):
        st.toast("Feature Unavailable: The Predictive Inference Engine (v2.0) is scheduled for the Q4 release.", icon="🚧")
