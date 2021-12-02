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
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

selectedCol = "Country"


def loadData(path=None) -> pd.DataFrame:
    if path is None:
        path = "https://raw.githubusercontent.com/glaand/Introduction-Programming-Dashboard/main/datasets/data.csv"
    return pd.read_csv(path).dropna()


def initApp() -> dash:
    appDash = dash.Dash(__name__)
    return appDash


def buildUserNav(data) -> list:
    dropdownOptions = getDropdownOptions(data)
    rows = getRows(data)
    return [html.H2("Dashboard Olympia Alex & André"),
            html.P("Visualising time series with Plotly - Dash"),
            html.P("Select the Data you want to plot."),
            dcc.Dropdown(id='columns-dropdown',
                         options=dropdownOptions,
                         value=dropdownOptions[0]["label"],
                         className='optionSelector'),
            dcc.Dropdown(id="rows-dropdown",
                         options=rows,
                         value=rows[0]["label"],
                         className="countrySelector")
            ]


def getDropdownOptions(df: pd.DataFrame) -> list:
    dict_list = []
    for i in list(df.columns.values):
        dict_list.append({"label": i, "value": i})
    return dict_list


def getRows(df: pd.DataFrame, key: str = None) -> list:
    if key is None:
        key = selectedCol
    dict_list = []
    for i in list(df[key].unique()):
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
                          color_discrete_sequence=["#FFD700", "#C0C0C0", "#CD7F32"]
                      )),
            dcc.Graph(id="scatter_geo",
                      config={"displayModeBar": False},
                      animate=True,
                      figure=px.scatter_geo(
                          data,
                          locations="Country_Code",
                          color="Medal",
                          projection="natural earth",
                          hover_name="Country",
                          hover_data={"Country": False, "Country_Code": False},
                          title="International Olympic Medals",
                          animation_frame="Year"
                      ))
            ]


def buildLayout(data) -> dash:
    return html.Div(children=[
        html.Div(className='row',  # Define the row element
                 children=[
                     html.Header(id="header"),
                     html.Div(className="four columns div-user-controls",
                              children=buildUserNav(data)),
                     html.Div(className="eight columns div-for-charts bg-grey",
                              children=buildStats(data)),
                     html.Footer(id="footer"),
                 ])
    ])


def main():
    df = loadData()
    app = initApp()
    app.layout = buildLayout(df)

    @app.callback(
        [Output(component_id='rows-dropdown', component_property='options')],
        [Input(component_id='columns-dropdown', component_property='value')]
    )
    def update_output_div(input_value):
        return getRows(df, input_value),

    app.run_server(debug=True, host="0.0.0.0", port=9999)


if __name__ == "__main__":
    main()
