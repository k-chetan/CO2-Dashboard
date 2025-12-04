
import streamlit as st
import plotly.graph_objects as go

def show(df):
    st.subheader("8. The Hope Story: Decoupling")
    st.markdown("""
    **The Key Insight:** Is it possible to get richer without getting dirtier? **Yes.**
    
    In the United States, the GDP (Green Line) has continued to skyrocket while Emissions (Red Line) have steadily declined since 2005. This proves that economic prosperity is no longer strictly tied to burning more fossil fuels.
    """)

    country = 'United States'
    subset = df[(df['country'] == country) & (df['year'] >= 1990)].copy()
    base_gdp = subset.iloc[0]['gdp']
    base_co2 = subset.iloc[0]['co2']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=subset['year'], y=(subset['gdp']/base_gdp)*100, mode='lines', name='GDP Growth', line=dict(color='#10B981', width=3)))
    fig.add_trace(go.Scatter(x=subset['year'], y=(subset['co2']/base_co2)*100, mode='lines', name='CO₂ Emissions', line=dict(color='#ef4444', width=3)))
    fig.update_layout(title=f"The Great Decoupling: {country} (1990=100)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"))
    st.plotly_chart(fig, use_container_width=True)
