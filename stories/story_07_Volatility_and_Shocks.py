
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("7. Volatility & Shocks")
    st.markdown("""
    **The Key Insight:** The environment breathes when the economy chokes.
    This chart shows the **Year-over-Year Growth Rate (%)**.
    
    Notice that the only times the line drops below zero (emissions reduction) are during massive human tragedies: the **2008 Financial Crisis** and the **COVID-19 Pandemic**.
    """)

    world_df = df[df['country'] == 'World'].sort_values('year')
    world_df['pct_change'] = world_df['co2'].pct_change() * 100
    subset = world_df[world_df['year'] > 1980]

    fig = px.bar(subset, x='year', y='pct_change', title="Annual Growth Rate (%)", color='pct_change', color_continuous_scale='RdYlGn_r')
    fig.add_hline(y=0, line_dash="solid", line_color="white")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
