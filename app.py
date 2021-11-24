#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Alexandru Schneider
# Created Date: 23. 11. 2021
# =============================================================================
# Dashboard App about Olympia data
# =============================================================================

# =============================================================================
# Imports
# =============================================================================
import os
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

DATA_PATH = os.path.join("datasets", "data.csv")


def loadData(path=None) -> pd.DataFrame:
    if path is None:
        path = DATA_PATH
    with open(path) as file:
        return pd.read_csv(file).dropna()


def initApp() -> dash:
    appDash = dash.Dash(__name__)
    appDash.layout = html.Div()
    return appDash


def buildUserNav(data) -> list:
    return [html.H2("Dashboard Olympia Alex & André"),
            html.P("Visualising time series with Plotly - Dash"),
            html.P("Select the Data you want to plot."),
            dcc.Dropdown(id='columns-dropdown',
                         options=getDropdownOptions(data),
                         value="Year",
                         style={'backgroundColor': '#1E1E1E'},
                         className='optionSelector'),
            dcc.Dropdown(id="country-dropdown",
                         options=getCountries(data),
                         value="Switzerland",
                         style={'backgroundColor': '#1E1E1E'},
                         className="countrySelector")
            ]


def getDropdownOptions(df: pd.DataFrame) -> list:
    dict_list = []
    for i in list(df.columns.values):
        dict_list.append({"label": i, "value": i})
    return dict_list


def getCountries(df: pd.DataFrame) -> list:
    dict_list = []
    for i in list(df["Country"].unique()):
        dict_list.append({"label": i, "value": i})
    return dict_list

def buildStats(data) -> list:
    return [dcc.Graph(id="scatter",
                      config={'displayModeBar': False},
                      animate=True,
                      figure=px.scatter(
                          data,
                          x="Country",
                          y="Discipline",
                          color="Medal",
                          # Colors: Gold = FFD700 | Silver = C0C0C0 | Bronze = CD7F32
                          color_discrete_sequence=["#FFD700", "#C0C0C0", "#CD7F32"],
                          template="plotly_dark"
                      ).update_layout(
                          {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                           'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
                      ).update_xaxes(
                          showgrid=True,
                          gridwidth=1,
                          gridcolor="gray"
                      ).update_yaxes(
                          showgrid=True,
                          gridwidth=1,
                          gridcolor="gray"
                      ))
            ]


def buildLayout(data) -> dash:
    return html.Div(children=[
        html.Div(className='row',  # Define the row element
                 children=[
                     html.Div(className="four columns div-user-controls",
                              children=buildUserNav(data)),
                     html.Div(className="eight columns div-for-charts bg-grey",
                              children=buildStats(data)),
                 ])
    ])


def main():
    df = loadData()
    app = initApp()
    app.layout = buildLayout(df)
    app.run_server(debug=True, host="0.0.0.0", port=9999)


if __name__ == "__main__":
    main()
