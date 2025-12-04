
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("4. Today's Heavy Hitters")
    st.markdown("""
    **The Key Insight:** This chart captures the "Passing of the Torch."
    For the entire 20th century, the US and Europe were the dominant emitters.
    
    However, look at the crossover point around **2006**. This is when China's rapid industrialization saw it overtake the US as the world's largest annual emitter. Meanwhile, US and EU emissions have essentially plateaued or declined.
    """)

    top_countries = ['China', 'United States', 'India', 'Russia', 'Japan', 'Germany']
    subset = df[df['country'].isin(top_countries)]

    fig = px.line(subset, x='year', y='co2', color='country', title="Annual Emissions: The Geopolitical Shift (1950-Present)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), xaxis=dict(showgrid=False), yaxis=dict(gridcolor='rgba(128,128,128,0.2)'))
    st.plotly_chart(fig, use_container_width=True)
