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
import pandas as pd
import os
import dash
import plotly.express as px
from dash import dcc
from dash import html
from typing import Tuple


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


if __name__ == "__main__":
    def exercise36():
        # Exercise 36
        student1, student2 = getAuthors()
        printAuthors()
    # exercise36()

    def exercise37():
        # Exercise 37
        df = load_data()
        print(df.head())
        row, col = getNumRowAndCol(df)
        print(f"{row} Datensätze mit {col} Spalten.")
    # exercise37()

    def exercise38():
        # Exercise 38
        df = load_data()
        filteredByCountry = filterDF(data=df, column="Country", key="Switzerland")
        filteredByDiscipline = filterDF(data=df, column="Discipline", key="Judo")
        print(f"a) Daten gefiltert nach dem Land Schweiz: \n{filteredByCountry} \nb) Daten gefiltert nach Disciplin Judo: \n{filteredByDiscipline}")

        app = dash.Dash(__name__)
        app.layout = html.Div([
            html.Title("Verbindung Disziplin mit Land:"),
            dcc.Graph(
                id="graph", 
                figure=px.scatter(df, 
                    x="Country",
                    y="Discipline",
                    color="Medal",
                    # Farben für Punkte: Gold = FFD700 | Silber = C0C0C0 | Bronze = CD7F32
                    color_discrete_sequence=["#FFD700", "#C0C0C0", "#CD7F32"]
                )

            ),
        ])

        app.run_server(debug=True, host="0.0.0.0", port=9999)

    exercise38()

    def exercise39():
        pass

    # exercise39()