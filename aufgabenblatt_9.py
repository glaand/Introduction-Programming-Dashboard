#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Alexandru Schneider
# Credits     : André Glatzl
# Created Date: 01. 12. 2021
# =============================================================================
"""Aufgabenblatt 9"""

# =============================================================================
# Imports
# =============================================================================
import pandas as pd
import numpy as np
from dash import dcc, Output, Input
from dash import html
import plotly.express as px
from aufgabenblatt_8 import showDash
import plotly.graph_objects as go


def load_data(path=None) -> pd.DataFrame:
    # Data is loaded from GitHub Repo
    if path is None:
        path = "https://raw.githubusercontent.com/glaand/Introduction-Programming-Dashboard/main/datasets/data.csv"
    return pd.read_csv(path).dropna()


def getSortedListByColumnName(df: pd.DataFrame, columnName: str) -> list:
    return sorted(list(df[columnName].unique()))


def getCountriesByDiscipline(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["Country", "Discipline"]).size().reset_index(name="Count").sort_values(by=["Count"], ascending=False)


def normalise(row, countriesByMedalSum: pd.DataFrame) -> pd.Series:
    try:
        row["Count"] = float(row["Count"] / countriesByMedalSum[countriesByMedalSum["Country"] == row["Country"]]["Count"])
    except KeyError:
        row["Count"] = 0.0
    except ZeroDivisionError:
        row["Count"] = 1.0
    return row


def aufgabe41(df: pd.DataFrame, toPrint=False):
    laender = getSortedListByColumnName(df, "Country")
    gewinner = getSortedListByColumnName(df, "Athlete")
    sportarten = getSortedListByColumnName(df, "Discipline")
    if toPrint:
        print(f"{laender}\n{gewinner}\n{sportarten}\n")
        print(f"Es gibt {len(laender)} Länder. \nEs gibt {len(gewinner)} Medaillengewinner. \nEs gibt {len(sportarten)} Disziplinen.")


def aufgabe42(df: pd.DataFrame, toPrint=False) -> pd.DataFrame:
    countriesByMedalSum = df.groupby(["Country"]).size().reset_index(name="Count")
    countriesByMedalSum = countriesByMedalSum.sort_values(by=["Count"], ascending=False)
    if toPrint:
        print(countriesByMedalSum.head(10))
    return countriesByMedalSum


def aufgabe43(df: pd.DataFrame, toPrint=False) -> pd.DataFrame:
    matrix = df.pivot(index="Discipline", columns="Country", values="Count")
    matrix = matrix.replace(to_replace =np.nan, value =0.) 
    if toPrint:
        print(matrix)
    return matrix


def aufgabe44(df: pd.DataFrame):
    countriesByMedalSum = aufgabe42(df)
    normalised = getCountriesByDiscipline(df)
    normalised = normalised.apply(
        lambda row: normalise(row, countriesByMedalSum),
        axis=1
    )
    matrix = aufgabe43(normalised)
    fig = go.Figure(
        go.Heatmap(
            x=matrix.columns.tolist(),
            y=matrix.index.tolist(),
            z=matrix.to_numpy()
        )
    )
    fig['layout']['xaxis']['type'] = 'category'
    fig['layout']['yaxis']['type'] = 'category'
    fig.update_layout(height=450)

    app = showDash([
            html.H1("Aufgabe 44"),
            html.H2("Farbkodierte Matrixvisualisierung"),
            dcc.Graph(
                id="heatmap", 
                figure=fig,
            ),
        ])
    return app, fig


def aufgabe45(df, fig):
    app = showDash([
        html.H1("Aufgabe 45"),
        html.Div(
            children=[
                html.H2("Mehrere Graphen darstellen"),
                dcc.Dropdown(
                    id="gender_dropdown",
                    options=[
                        {"label": "Men", "value": "Men"},
                        {"label": "Women", "value": "Women"},
                    ],
                    value="Men"
                ),
                dcc.Graph(
                    id="bar",
                ),
                dcc.Slider(
                    id='year_slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=df['Year'].max(),
                    marks={str(int(year)): str(int(year)) for year in df["Year"].unique()},
                    step=4
                ),
            ],
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H3("Grafik Nummer 2"),
                        dcc.Graph(
                            id="heatmap",
                            figure=fig,
                        ),
                    ],
                    className="graph"
                ),
                html.Div(
                    children=[
                        html.H3("Grafik Nummer 3"),
                        dcc.Graph(
                            id="line",
                            figure=px.scatter(
                                    df,
                                    x="Country",
                                    y="Discipline",
                                    color="Medal",
                                    # Farben für Punkte: Gold = FFD700 | Silber = C0C0C0 | Bronze = CD7F32
                                    color_discrete_sequence=["#FFD700", "#C0C0C0", "#CD7F32"]
                                ),
                        ),
                    ],
                    className="graph"
                )
            ],
            className="flex"
        )
    ], "aufgabe45")

    @app.callback(
        [Output("bar", "figure")],
        [Input("gender_dropdown", "value"),
         Input("year_slider", "value")]
    )
    def updateBarGraph(gender, year_value):
        # Dataframe should contain, men/women and their respective medal count per year
        dff = df.groupby(["Year", "Gender"]).size().reset_index(name="Count")
        # select either male or female (men/women)
        dff = dff[dff["Gender"] == gender]
        # dataframe drops the years which arent needed
        dff = dff.drop(dff[dff.Year > year_value].index)
        fig = px.bar(dff,
                      x="Year",
                      y="Count",
                      title=f"Anzahl Medaillen der {'Männer' if gender == 'Men' else 'Frauen'}",)
        fig.update_xaxes(type='category')
        return fig,

    return app


def main():
    df = load_data()
    # aufgabe41(df)
    # aufgabe42(df)
    # aufgabe43(getCountriesByDiscipline(df))
    app2, fig = aufgabe44(df)
    app = aufgabe45(df, fig)

    app.run_server(debug=True, host="0.0.0.0", port=9999)


if __name__ == "__main__":
    main()
