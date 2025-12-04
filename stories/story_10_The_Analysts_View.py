
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("10. The Analyst's View: Wealth, Pop, & CO₂")
    st.markdown("""
    **The Key Insight:** This bubble chart brings it all together. 
    * **X-Axis:** Wealth (GDP per Capita).
    * **Y-Axis:** Annual Emissions (Log Scale).
    * **Bubble Size:** Population.
    
    The trend is clear: As nations move right (get richer), they tend to move up (emit more). The challenge is to help the massive bubbles at the bottom left move *right* without shooting *up*.
    """)

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
