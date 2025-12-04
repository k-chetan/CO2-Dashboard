
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("5. The Great Acceleration")
    st.markdown("""
    **The Key Insight:** This is a zero-sum game view. It shows the *percentage share* of global emissions.
    
    The visualization reveals a massive squeeze. In 1950, the US and Europe (OECD) accounted for the vast majority of the pie. Today, their ribbons are shrinking, squeezed out by the expanding share of the "Rest of the World" (Asia, Africa, Latin America).
    """)

    top_countries = ['China', 'United States', 'India', 'Russia', 'Japan']
    subset = df[df['country'].isin(top_countries)]
    
    fig = px.area(subset, x='year', y='share_global_co2', color='country', title="Share of Global Total Emissions (%)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), yaxis=dict(gridcolor='rgba(128,128,128,0.2)'))
    st.plotly_chart(fig, use_container_width=True)
