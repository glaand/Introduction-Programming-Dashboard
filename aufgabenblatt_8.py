#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : André Glatzl
# Credits     : Alexandru Schneider
# Created Date: 18. 11. 2021
# =============================================================================
"""Aufgabenblatt 8"""

# =============================================================================
# Imports
# =============================================================================
from io import TextIOWrapper
import pandas as pd
import numpy as np
import os
import dash
import plotly.express as px
from dash import dcc
from dash import html
from typing import Tuple
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# =============================================================================
# Constants
# =============================================================================
DATA_PATH = os.path.join("datasets", "data.csv")


# =============================================================================
# Exercise 36
# =============================================================================
def getAuthors() -> Tuple[str, str]:
    student1 = "André Glatzl"
    student2 = "Alexandru Schneider"
    return student1, student2


def printAuthors() -> None:
    student1, student2 = getAuthors()
    print(f"Die Projektgruppe besteht aus {student1} und {student2}.")


# =============================================================================
# Exercise 37
# =============================================================================
def load_data(path=None) -> pd.DataFrame:
    if path is None:
        path = DATA_PATH
    with open(path) as file:
        return pd.read_csv(file).dropna()


def getNumRowAndCol(dataFrame) -> Tuple[int, int]:
    return len(dataFrame), len(dataFrame.columns)


# =============================================================================
# Exercise 38
# =============================================================================
def filterDF(**kwargs) -> pd.DataFrame:
    # keywords: data=dataFrame, column=Spalte, key=Suchwert
    if kwargs['column'] not in list(kwargs['data'].columns): 
        print(f"Given column {kwargs['column']} is not in Data.")
        return pd.DataFrame([])
    return kwargs['data'].loc[kwargs['data'][kwargs['column']] == kwargs['key']]

# =============================================================================
# Exercise 39 & 40
# =============================================================================
def showDash(elements: list, className=""):
    app = dash.Dash(__name__)
    app.layout = html.Div(elements, className=className)
    return app, app.server


def getRows(df: pd.DataFrame, key: str = None) -> list:
    dict_list = []
    for i in list(df[key].unique()):
        dict_list.append({"label": i, "value": i})
    return dict_list


def get_axis(df, medal, key):
    r = df[df["Medal"] == medal][key]
    if key == "Year":
        r = np.sort(r.unique())
    return r

def exercise36():
    # Exercise 36
    student1, student2 = getAuthors()
    printAuthors()

def exercise37():
    # Exercise 37
    df = load_data()
    print(df.head())
    row, col = getNumRowAndCol(df)
    print(f"{row} Datensätze mit {col} Spalten.")

def exercise38(toPrint=True):
    # Exercise 38
    df = load_data()
    filteredByCountry = filterDF(data=df, column="Country", key="Switzerland")
    filteredByDiscipline = filterDF(data=df, column="Discipline", key="Judo")
    if toPrint:
        print(f"a) Daten gefiltert nach dem Land Schweiz: \n{filteredByCountry} \nb) Daten gefiltert nach Disciplin Judo: \n{filteredByDiscipline}")

    app = showDash([
        html.P("Aufgabe 38"),
        html.P("Verbindung Disziplin mit Land:"),
        dcc.Graph(
            id="graph", 
            figure=px.scatter(
                df, 
                x="Country",
                y="Discipline",
                color="Medal",
                # Farben für Punkte: Gold = FFD700 | Silber = C0C0C0 | Bronze = CD7F32
                color_discrete_sequence=["#FFD700", "#C0C0C0", "#CD7F32"]
            )

        ),
    ])
    return app

def exercise39():
    df = load_data()
    # Filter to only show One Country
    df2 = filterDF(data=df, column="Country", key="Switzerland")
    # Filter to only display Gold 
    df3 = filterDF(data=df2, column="Medal", key="Gold")
    # Group all the Gold Medals per Year
    df4 = df3.groupby(["Year"]).size().reset_index(name="Gold")
    app = showDash([
        html.P("Aufgabe 39"),
        html.P("Streudiagramm: Land pro Disziplin"),
        dcc.Graph(
            id="scatter", 
            figure=px.scatter(
                df, 
                x="Country",
                y="Discipline",
                color="Medal",
                # Farben für Punkte: Gold = FFD700 | Silber = C0C0C0 | Bronze = CD7F32
                color_discrete_sequence=["#FFD700", "#C0C0C0", "#CD7F32"]
            )
        ),
        html.P("Histogramm von Anzahl Medaillen pro Land"),
        dcc.Graph(
            id="histo", 
            figure=px.histogram(
                df, 
                x="Country",
            )
        ),
        html.P("Liniendiagramm: Anzahl Gold-Medaillen von der Schweiz über die Jahre"),
        dcc.Graph(
            id="line", 
            figure=px.line(
                df4, 
                x="Year",
                y="Gold",
            )
        ),
    ])
    return app

def exercise40():
    df = load_data()
    df2 = df.groupby(["Country", "Year", "Medal"]).size().reset_index(name="count")
    rows = getRows(df2, "Country")
    df2["Year"] = df2["Year"].astype(int)
    appTuple = showDash([
        html.P("Aufgabe 40"),
        html.P("Gestapeltes Balkendiagramm: Anzahl Medaillen pro Land (Mit Dropdown)"),
        dcc.Dropdown(
            id="country",
            options=rows,
            value=rows[0]["label"],
        ),
        dcc.Graph(
            id="line-chart", 
            figure={}
        )
    ])

    app, server = appTuple

    @app.callback(
        Output(component_id='line-chart', component_property='figure'),
        Input(component_id='country', component_property='value'),
    )
    def update_graph(country):
        ctx = dash.callback_context
        print(ctx)

        dff = df2.copy()
        dff2 = dff[dff["Country"] == country]
        for y in range(1976, 2012, 4):
            a_row = pd.Series({"Country": country, "Year": y, "Medal": "Bronze", "count": 0})
            row_df = pd.DataFrame([a_row])
            dff2 = pd.concat([row_df, dff2], ignore_index=True)
        dff2 = dff2.loc[dff2.reset_index().groupby(["Country", "Year", "Medal"])["count"].idxmax()]
        bronze_x = get_axis(dff2, "Bronze", "Year")
        bronze_y = get_axis(dff2, "Bronze", "count").to_numpy()
        silver_x = get_axis(dff2, "Silver", "Year")
        silver_y = get_axis(dff2, "Silver", "count").to_numpy()
        gold_x = get_axis(dff2, "Gold", "Year")
        gold_y = get_axis(dff2, "Gold", "count").to_numpy()

        fig = go.Figure(data=[
            go.Bar(
                name='Bronze', 
                x=bronze_x,
                y=bronze_y,
                marker={"color": "#CD7F32"},
            ),
            go.Bar(
                name='Silver', 
                x=silver_x,
                y=silver_y,
                marker={"color": "#C0C0C0"},
            ),
            go.Bar(
                name='Gold', 
                x=gold_x,
                y=gold_y,
                marker={"color": "#FFD700"}
            ),
        ])
        fig.update_xaxes(title="Olympic year", type="category")
        fig.update_yaxes(title="Medal count", dtick=1, type="log")

        # Change the bar mode
        fig.update_layout(
            barmode='stack'
        )
        return fig
    return app

if __name__ == "__main__":
    exercise36()
    exercise37()
    # application = exercise38()
    # application = exercise39()
    application = exercise40()
    # Open Web Browser and type "localhost:9999" and hit enter
    application.run_server(debug=True, host="0.0.0.0", port=9999)

