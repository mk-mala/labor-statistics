import streamlit as st
import time
import pandas as pd
import numpy as np
import duckdb
import plotly.express as px

import utils.utilities as utilities

##############################################################################
# Datasets

conn = duckdb.connect('data/labor_statistics.db')

df_labor_force = conn.execute("SELECT * FROM local_area_employment__labor_force").fetchdf()
df_industry = conn.execute("SELECT * FROM local_area_employment__industry").fetchdf()

##############################################################################
# Sidebar

with st.sidebar:

    ls_states = list(sorted(set(df_labor_force['state'])))
    #ls_areas = list(set(df_labor_force['area'].sort_values(ascending=False)))

    option_state = st.selectbox(
        "Select a State:",
        ls_states
    )

    ls_areas = list(sorted(set(df_labor_force[df_labor_force['state'] == option_state]['area'])))

    option_area = st.selectbox(
        "Select an Area:",
        ls_areas
    )

##############################################################################
# Local Area Dataset

df_labor_force = df_labor_force[df_labor_force['area'] == option_area]

df_industry = df_industry[df_industry['area'] == option_area]

##############################################################################
# Title & Subheader

st.title("Local Area Economy")
st.subheader(df_labor_force[df_labor_force['area'] == option_area].iloc[0]['area'])

##############################################################################
# Current Metrics

col1, col2, col3, col4 = st.columns(4)

# Values
current_labor_force = f'{df_labor_force.iloc[-1]['labor_force']:,}' 
current_employment = f'{df_labor_force.iloc[-1]['employment']:,}' 
current_unemployment = f'{df_labor_force.iloc[-1]['unemployment']:,}' 
current_unemployment_rate = f'{df_labor_force.iloc[-1]['unemployment_rate']:,.2f}%'

# Deltas
delta_labor_force = f'{df_labor_force.iloc[-1]['delta_labor_force']:,}' 
delta_employment = f'{df_labor_force.iloc[-1]['delta_employment']:,}' 
delta_unemployment = f'{df_labor_force.iloc[-1]['delta_unemployment']:,}' 
delta_unemployment_rate = f'{df_labor_force.iloc[-1]['delta_unemployment_rate']:,.2f}%' 

# Metrics
col1.metric("Labor Force", current_labor_force, delta_labor_force)
col2.metric("Employment", current_employment, delta_employment)
col3.metric("Unemployment", current_unemployment, delta_unemployment)
col4.metric("Unemployment Rate", current_unemployment_rate, delta_unemployment_rate)

##############################################################################
# Labor Force

with st.container(border=True):

    tab1, tab2, tab3, tab4 = st.tabs(['Labor Force', 'Employment', 'Unemployment', 'Unemployment Rate'],)

    with tab1:

            fig_labor_force = utilities.create_line_chart(
                df_labor_force,
                x_axis='date',
                y_axis='labor_force',
                title=df_labor_force.iloc[0]['area'],
                x_axis_title='Date',
                y_axis_title='Labor Force'
            )

            st.plotly_chart(fig_labor_force)

    with tab2:

        fig_employment = utilities.create_line_chart(
            df_labor_force,
            x_axis='date',
            y_axis='employment',
            title=df_labor_force.iloc[0]['area'],
            x_axis_title='Date',
            y_axis_title='Employment'
        )

        st.plotly_chart(fig_employment)

    with tab3:

        fig_unemployment = utilities.create_line_chart(
            df_labor_force,
            x_axis='date',
            y_axis='unemployment',
            title=df_labor_force.iloc[0]['area'],
            x_axis_title='Date',
            y_axis_title='Unemployment'
        )

        st.plotly_chart(fig_unemployment)

    with tab4:

        fig_unemployment_rate = utilities.create_line_chart(
            df_labor_force,
            x_axis='date',
            y_axis='unemployment_rate',
            title=df_labor_force.iloc[0]['area'],
            x_axis_title='Date',
            y_axis_title='Unemployment Rate (%)'
        )

        st.plotly_chart(fig_unemployment_rate)

##############################################################################
# Industry

with st.container(border=True):

    ls_industries = sorted(list(set(df_industry['industry'])))

    option_industry = st.selectbox(
        "Select an Industry",
        ls_industries
    )

    fig_industry = utilities.create_line_chart(
        df_industry[df_industry['industry'] == option_industry],
        x_axis='date',
        y_axis='non_farm_payrolls',
        title=option_industry,
        x_axis_title='Date',
        y_axis_title='Non-Farm Payrolls'
    )

    st.plotly_chart(fig_industry)
