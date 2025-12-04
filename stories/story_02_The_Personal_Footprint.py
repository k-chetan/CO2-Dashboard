
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("2. The Personal Footprint")
    st.markdown("""
    **The Key Insight:** Maps of *total* emissions often just show us where people live. 
    To understand lifestyle impact, we must look at **Per Capita** emissions.
    
    This scatter plot reveals a stark inequality: Residents of nations like the **USA, Australia, and Canada** emit 10x-15x more per person than residents of India or Nigeria. A high standard of living is currently deeply correlated with a high individual carbon footprint.
    """)

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
