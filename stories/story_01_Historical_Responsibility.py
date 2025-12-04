
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("1. The Long Shadow: Historical Responsibility")
    st.markdown("""
    **The Key Insight:** Climate change is a stock problem, not just a flow problem. 
    While China is the largest *current* emitter, CO₂ persists in the atmosphere for centuries. 
    
    When we sum up every tonne of CO₂ emitted since 1750, the picture changes. The **United States** and **Europe** hold the majority of historical responsibility for the carbon currently warming our planet. 
    This data is the mathematical basis for "Climate Justice" debates at UN summits.
    """)

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
