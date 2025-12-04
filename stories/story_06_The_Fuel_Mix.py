
import streamlit as st
import plotly.express as px

def show(df):
    st.subheader("6. The Fuel Mix: The Hidden Giant")
    st.markdown("""
    **The Key Insight:** To decarbonize, we have to know what we are burning. 
    The terrifying reality shown here is the dominance of **Coal** (the dark grey area).
    
    Despite the headlines about wind and solar, the global industrial baseload—especially in rapidly developing economies—is still largely powered by burning solid rock.
    """)

    subset = df[df['country'] == 'World']
    melted = subset.melt(id_vars=['year'], value_vars=['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2'], var_name='Fuel', value_name='Emissions')
    melted['Fuel'] = melted['Fuel'].str.replace('_co2', '').str.capitalize()
    
    fuel_colors = {'Coal': '#2d3748', 'Oil': '#4b5563', 'Gas': '#10B981', 'Cement': '#9ca3af', 'Flaring': '#f59e0b'}
    fig = px.area(melted, x='year', y='Emissions', color='Fuel', title="Global Emissions by Source (1950-Present)", color_discrete_map=fuel_colors)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), xaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True)
