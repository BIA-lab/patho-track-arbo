import streamlit as st
import plotly.express as px
from utils.dicts import main_lineages_color_scheme, concerned_variants
from datetime import datetime, timedelta
import pandas as pd

# new libs
import plotly.graph_objs as go
import plotly.io as pio


def variants_bar_plot(variants_percentage, column, title, pivot_df):
    c = column

    with st.container():
        c.subheader(title)
    
        pio.renderers.default = "browser" 
        # NOW WE CAN FINALLY MAKE THE CHART
        traces = []
        for v in variants_percentage:
            trace = go.Bar(
                x = pivot_df.index,
                y = pivot_df[v],
                name = v[8:]
            ) 
            
            traces.append(trace)

        layout = go.Layout(
            title = "   ",
            barmode = "stack",
            xaxis = dict(title = "Year"),
            yaxis = dict(title = "Proportion of Genomes",
                        tickformat = "%",
                        hoverformat = "%"),
            legend = dict(
                title = dict(text = "Serotypes", font = dict(size = 16)))     
        )

        fig = go.Figure(traces, layout)
        c.plotly_chart(fig, use_container_width=True)
        
