
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("3. The Global Trend")
    st.markdown("""
    **The Key Insight:** This is the curve of the "Great Acceleration."
    Since 1950, global emissions have not just risen; they have exploded. 
    
    Notice the resilience of this trend. Major events like the **2008 Financial Crisis** or the **COVID-19 pandemic** appear only as tiny, temporary blips. The structural dependency of the global economy on fossil fuels means that emissions rebound almost immediately after every crisis.
    """)

    world_df = df[df['country'] == 'World']
    fig = px.line(world_df, x='year', y='co2', title="Global Annual CO₂ Emissions (1950-Present)",
        labels={'co2': 'Annual CO₂ (Million Tonnes)'}, color_discrete_sequence=['#10B981'])
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), xaxis=dict(showgrid=False), yaxis=dict(gridcolor='rgba(128,128,128,0.2)'))
    st.plotly_chart(fig, use_container_width=True)
