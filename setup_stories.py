import os
import shutil

# 1. Define the directory
stories_dir = "stories"
pages_dir = "pages"

# 2. Clean up old 'pages' directory if it exists (Fixes the Sidebar Glitch)
if os.path.exists(pages_dir):
    print(f"Removing conflicting '{pages_dir}' directory...")
    shutil.rmtree(pages_dir)

# 3. Create 'stories' directory
if not os.path.exists(stories_dir):
    os.makedirs(stories_dir)
    print(f"Created '{stories_dir}' directory.")

# 4. Create __init__.py (Fixes the Import Error)
with open(os.path.join(stories_dir, "__init__.py"), "w") as f:
    pass 

# 5. Define the Content for All 10 Stories
stories_content = {
    "story_01_Historical_Responsibility.py": """
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("1. The Long Shadow: Historical Responsibility")
    st.markdown(\"\"\"
    **The Key Insight:** Climate change is a stock problem, not just a flow problem. 
    While China is the largest *current* emitter, CO₂ persists in the atmosphere for centuries. 
    
    When we sum up every tonne of CO₂ emitted since 1750, the picture changes. The **United States** and **Europe** hold the majority of historical responsibility for the carbon currently warming our planet. 
    This data is the mathematical basis for "Climate Justice" debates at UN summits.
    \"\"\")

    latest_year = df['year'].max()
    current_df = df[df['year'] == latest_year].sort_values('cumulative_co2', ascending=False)
    country_df = current_df[current_df['iso_code'] != 0].head(15)

    fig = px.bar(
        country_df, x='cumulative_co2', y='country', orientation='h',
        title=f"Total Cumulative Emissions (1750-{latest_year})",
        labels={'cumulative_co2': 'Cumulative CO₂ (Million Tonnes)', 'country': ''},
        color='cumulative_co2', color_continuous_scale='Greens'
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_02_The_Personal_Footprint.py": """
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("2. The Personal Footprint")
    st.markdown(\"\"\"
    **The Key Insight:** Maps of *total* emissions often just show us where people live. 
    To understand lifestyle impact, we must look at **Per Capita** emissions.
    
    This scatter plot reveals a stark inequality: Residents of nations like the **USA, Australia, and Canada** emit 10x-15x more per person than residents of India or Nigeria. A high standard of living is currently deeply correlated with a high individual carbon footprint.
    \"\"\")

    curr_df = df[df['year'] == 2022]
    subset = curr_df[(curr_df['population'] > 1000000) & (curr_df['iso_code'] != 0)]

    fig = px.scatter(
        subset, x='gdp', y='co2_per_capita', size='population', color='country',
        hover_name='country', log_x=True, size_max=60,
        title="Wealth vs. Personal Carbon Footprint (2022)",
        labels={'gdp': 'GDP (Log Scale)', 'co2_per_capita': 'CO₂ Per Person (Tonnes)'}
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_03_The_Global_Trend.py": """
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("3. The Global Trend")
    st.markdown(\"\"\"
    **The Key Insight:** This is the curve of the "Great Acceleration."
    Since 1950, global emissions have not just risen; they have exploded. 
    
    Notice the resilience of this trend. Major events like the **2008 Financial Crisis** or the **COVID-19 pandemic** appear only as tiny, temporary blips. The structural dependency of the global economy on fossil fuels means that emissions rebound almost immediately after every crisis.
    \"\"\")

    world_df = df[df['country'] == 'World']
    fig = px.line(world_df, x='year', y='co2', title="Global Annual CO₂ Emissions (1950-Present)",
        labels={'co2': 'Annual CO₂ (Million Tonnes)'}, color_discrete_sequence=['#10B981'])
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), xaxis=dict(showgrid=False), yaxis=dict(gridcolor='rgba(128,128,128,0.2)'))
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_04_Todays_Heavy_Hitters.py": """
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("4. Today's Heavy Hitters")
    st.markdown(\"\"\"
    **The Key Insight:** This chart captures the "Passing of the Torch."
    For the entire 20th century, the US and Europe were the dominant emitters.
    
    However, look at the crossover point around **2006**. This is when China's rapid industrialization saw it overtake the US as the world's largest annual emitter. Meanwhile, US and EU emissions have essentially plateaued or declined.
    \"\"\")

    top_countries = ['China', 'United States', 'India', 'Russia', 'Japan', 'Germany']
    subset = df[df['country'].isin(top_countries)]

    fig = px.line(subset, x='year', y='co2', color='country', title="Annual Emissions: The Geopolitical Shift (1950-Present)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), xaxis=dict(showgrid=False), yaxis=dict(gridcolor='rgba(128,128,128,0.2)'))
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_05_The_Great_Acceleration.py": """
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("5. The Great Acceleration")
    st.markdown(\"\"\"
    **The Key Insight:** This is a zero-sum game view. It shows the *percentage share* of global emissions.
    
    The visualization reveals a massive squeeze. In 1950, the US and Europe (OECD) accounted for the vast majority of the pie. Today, their ribbons are shrinking, squeezed out by the expanding share of the "Rest of the World" (Asia, Africa, Latin America).
    \"\"\")

    top_countries = ['China', 'United States', 'India', 'Russia', 'Japan']
    subset = df[df['country'].isin(top_countries)]
    
    fig = px.area(subset, x='year', y='share_global_co2', color='country', title="Share of Global Total Emissions (%)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), yaxis=dict(gridcolor='rgba(128,128,128,0.2)'))
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_06_The_Fuel_Mix.py": """
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("6. The Fuel Mix: The Hidden Giant")
    st.markdown(\"\"\"
    **The Key Insight:** To decarbonize, we have to know what we are burning. 
    The terrifying reality shown here is the dominance of **Coal** (the dark grey area).
    
    Despite the headlines about wind and solar, the global industrial baseload—especially in rapidly developing economies—is still largely powered by burning solid rock.
    \"\"\")

    subset = df[df['country'] == 'World']
    melted = subset.melt(id_vars=['year'], value_vars=['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2'], var_name='Fuel', value_name='Emissions')
    melted['Fuel'] = melted['Fuel'].str.replace('_co2', '').str.capitalize()
    
    fuel_colors = {'Coal': '#2d3748', 'Oil': '#4b5563', 'Gas': '#10B981', 'Cement': '#9ca3af', 'Flaring': '#f59e0b'}
    fig = px.area(melted, x='year', y='Emissions', color='Fuel', title="Global Emissions by Source (1950-Present)", color_discrete_map=fuel_colors)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), xaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_07_Volatility_and_Shocks.py": """
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("7. Volatility & Shocks")
    st.markdown(\"\"\"
    **The Key Insight:** The environment breathes when the economy chokes.
    This chart shows the **Year-over-Year Growth Rate (%)**.
    
    Notice that the only times the line drops below zero (emissions reduction) are during massive human tragedies: the **2008 Financial Crisis** and the **COVID-19 Pandemic**.
    \"\"\")

    world_df = df[df['country'] == 'World'].sort_values('year')
    world_df['pct_change'] = world_df['co2'].pct_change() * 100
    subset = world_df[world_df['year'] > 1980]

    fig = px.bar(subset, x='year', y='pct_change', title="Annual Growth Rate (%)", color='pct_change', color_continuous_scale='RdYlGn_r')
    fig.add_hline(y=0, line_dash="solid", line_color="white")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_08_The_Hope_Story_Decoupling.py": """
import streamlit as st
import plotly.graph_objects as go

def show(df):
    st.subheader("8. The Hope Story: Decoupling")
    st.markdown(\"\"\"
    **The Key Insight:** Is it possible to get richer without getting dirtier? **Yes.**
    
    In the United States, the GDP (Green Line) has continued to skyrocket while Emissions (Red Line) have steadily declined since 2005. This proves that economic prosperity is no longer strictly tied to burning more fossil fuels.
    \"\"\")

    country = 'United States'
    subset = df[(df['country'] == country) & (df['year'] >= 1990)].copy()
    base_gdp = subset.iloc[0]['gdp']
    base_co2 = subset.iloc[0]['co2']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=subset['year'], y=(subset['gdp']/base_gdp)*100, mode='lines', name='GDP Growth', line=dict(color='#10B981', width=3)))
    fig.add_trace(go.Scatter(x=subset['year'], y=(subset['co2']/base_co2)*100, mode='lines', name='CO₂ Emissions', line=dict(color='#ef4444', width=3)))
    fig.update_layout(title=f"The Great Decoupling: {country} (1990=100)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"))
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_09_Consumption_vs_Production.py": """
import streamlit as st
import plotly.graph_objects as go

def show(df):
    st.subheader("9. Offshoring Pollution")
    st.markdown(\"\"\"
    **The Key Insight:** Are rich countries really cleaning up, or are they just exporting their pollution?
    
    **Production Emissions** (Blue) calculate what is burned inside a country's borders. 
    **Consumption Emissions** (Orange) adjust for trade: they add the emissions of imported goods. For the UK, the "Clean" production line hides the truth: their consumption footprint is consistently higher.
    \"\"\")

    country = 'United Kingdom'
    subset = df[(df['country'] == country) & (df['year'] >= 1990)].dropna(subset=['consumption_co2'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=subset['year'], y=subset['co2'], fill='tozeroy', mode='none', name='Production', fillcolor='rgba(59, 130, 246, 0.5)'))
    fig.add_trace(go.Scatter(x=subset['year'], y=subset['consumption_co2'], mode='lines', name='Consumption', line=dict(color='#f97316', width=3)))
    fig.update_layout(title=f"The Trade Gap: {country}", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)
""",

    "story_10_The_Analysts_View.py": """
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("10. The Analyst's View: Wealth, Pop, & CO₂")
    st.markdown(\"\"\"
    **The Key Insight:** This bubble chart brings it all together. 
    * **X-Axis:** Wealth (GDP per Capita).
    * **Y-Axis:** Annual Emissions (Log Scale).
    * **Bubble Size:** Population.
    
    The trend is clear: As nations move right (get richer), they tend to move up (emit more). The challenge is to help the massive bubbles at the bottom left move *right* without shooting *up*.
    \"\"\")

    curr_df = df[df['year'] == 2018]
    subset = curr_df[(curr_df['gdp'] > 0) & (curr_df['co2'] > 0) & (curr_df['iso_code'] != 0)]
    subset['gdp_per_capita'] = subset['gdp'] / subset['population']

    fig = px.scatter(
        subset, x='gdp_per_capita', y='co2', size='population', color='country',
        hover_name='country', log_x=True, log_y=True, size_max=60,
        title="Multivariate Analysis: Wealth vs Emissions vs Population",
        labels={'gdp_per_capita': 'GDP per Capita (Log)', 'co2': 'Annual CO₂ (Log)'}
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
"""
}

# 6. Write the files
print("Writing 10 story modules...")
for filename, content in stories_content.items():
    path = os.path.join(stories_dir, filename)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Generated: {path}")

print("\n🎉 Success! The 'pages' folder is gone, and 'stories' is populated.")
print("👉 Run 'streamlit run app.py' now.")