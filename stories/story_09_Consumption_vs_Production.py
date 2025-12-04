
import streamlit as st
import plotly.graph_objects as go

def show(df):
    st.subheader("9. Offshoring Pollution")
    st.markdown("""
    **The Key Insight:** Are rich countries really cleaning up, or are they just exporting their pollution?
    
    **Production Emissions** (Blue) calculate what is burned inside a country's borders. 
    **Consumption Emissions** (Orange) adjust for trade: they add the emissions of imported goods. For the UK, the "Clean" production line hides the truth: their consumption footprint is consistently higher.
    """)

    country = 'United Kingdom'
    subset = df[(df['country'] == country) & (df['year'] >= 1990)].dropna(subset=['consumption_co2'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=subset['year'], y=subset['co2'], fill='tozeroy', mode='none', name='Production', fillcolor='rgba(59, 130, 246, 0.5)'))
    fig.add_trace(go.Scatter(x=subset['year'], y=subset['consumption_co2'], mode='lines', name='Consumption', line=dict(color='#f97316', width=3)))
    fig.update_layout(title=f"The Trade Gap: {country}", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)
