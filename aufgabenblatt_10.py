#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : André Glatzl
# Credits     : Alexandru Schneider
# Created Date: 16. 12. 2021
# =============================================================================
"""Aufgabenblatt 10"""

# =============================================================================
# Imports
# =============================================================================
from aufgabenblatt_8 import showDash
from aufgabenblatt_9 import load_data
import pandas as pd
from dash import html, dcc
import plotly.express as px


def filter_data(df: pd.DataFrame, land: str, jahr: int, sportart: str) -> pd.DataFrame:
    if land is not None:
        df = df[df["Country"] == land]
    if jahr is not None:
        df = df[df["Year"] == jahr]
    if sportart is not None:
        df = df[df["Sport"] == sportart]
    return df


def filter_data2(df, string: str):
    pattern = ""
    for char in string:
        pattern += f"(?=.*{str(char)})"
    pattern += ".*"
    return df[df["Athlete"].str.match(pattern)]


def group_medals_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    df = filter_data(df, country, None, None)
    df = df.groupby(["Country", "Medal"]).size().reset_index(name="Count")
    df = df.drop("Country", axis=1).set_index("Medal").transpose()
    return df


def aufgabe49(data: pd.DataFrame):
    df_usa = normalizeDataFrame(countMedalPerYearForCountry(data, "United States"))
    df_sov = normalizeDataFrame(countMedalPerYearForCountry(data, "Soviet Union"))
    df_wger = normalizeDataFrame(countMedalPerYearForCountry(data, "West Germany"))
    df_eger = normalizeDataFrame(countMedalPerYearForCountry(data, "East Germany"))
    df_dis = countDisciplinesPerYear(data).sort_values("Count")
    return showDash([
        html.H1("Aufgabe 49"),
        html.Div(
            children=[
                html.H3("Grafik 1 - USA fällt 1980 aus"),
                dcc.Graph(
                    id="USA_Bar",
                    figure=plotCountPerYearsForCountry(df_usa, "Anzahl Medaillen über alle Jahre USA")
                )
            ]
        ),
        html.Div(
            children=[
                html.H3("Grafik 2 - Soviet Union fällt 1984 aus und ab 1988 keine Medaillen mehr"),
                dcc.Graph(
                    id="SOV_bar",
                    figure=plotCountPerYearsForCountry(df_sov, "Anzahl Medaillen über alle Jahre Soviet Union")
                )
            ]
        ),
        html.Div(
            children=[
                html.H3("Grafik 3 - West Deutschland fällt 1980 aus und holt ab 1988 keine Medaillen mehr"),
                dcc.Graph(
                    id="WEST_GER_bar",
                    figure=plotCountPerYearsForCountry(df_wger, "Anzahl Medaillen über alle Jahre West Deutschland")
                )
            ]
        ),
        html.Div(
            children=[
                html.H3("Grafik 4 - Ost Deutschland fällt 1984 aus und holt ab 1988 keine Medaillen mehr"),
                dcc.Graph(
                    id="EAST_GER_bar",
                    figure=plotCountPerYearsForCountry(df_eger, "Anzahl Medaillen über alle Jahre Ost Deutschland")
                )
            ]
        ),
        html.Div(
            children=[
                html.H3("Grafik 5 - Soviet Union ist zweithöchster Medaillengewinner obwohl sie nur 3 mal teilgenommen haben!!"),
                dcc.Graph(
                    id="Countries_All_Years",
                    figure=px.bar(df_dis.tail(20),
                                  title="Top 20 Länder",
                                  x="Country",
                                  y="Count")
                )
            ]
        )
    ])


def countMedalPerYearForCountry(df: pd.DataFrame, country: str) -> pd.DataFrame:
    return filter_data(df, country, None, None).groupby("Year").size().reset_index(name="Count")


# some Countries didnt win medals every Olympic games
def normalizeDataFrame(df: pd.DataFrame) -> pd.DataFrame:
    normalizedDataFrame = pd.DataFrame(columns=["Year", "Count"])
    for year in range(1976, 2012, 4):
        dff = df[df["Year"] == year]
        # Falls in einem Jahr keine Medaillen geholt wurde
        if len(dff.index) != 0:
            count = dff.iloc[0, 1]
        else:
            count = 0
        rows = {"Year": year, "Count": count}
        normalizedDataFrame = normalizedDataFrame.append(rows, ignore_index=True)
    return normalizedDataFrame


def plotCountPerYearsForCountry(df: pd.DataFrame, title: str):
    figure = px.bar(
        df,
        title=title,
        x="Year",
        y="Count"
    )
    figure.update_xaxes(type="category")
    return figure


def countDisciplinesPerYear(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("Country").size().reset_index(name="Count")


def main():
    # load data from csv as dataframe
    data = load_data()
    # change Year column to integer
    data["Year"] = data["Year"].astype(int)

    # Aufgabe 46
    result_data_frame = filter_data(data, "Switzerland", 2008, "Cycling")
    print(f"Aufgabe 46: \n{result_data_frame.head()}")

    # Aufgabe 47
    searched_data_frame = filter_data2(data, "zv")
    print(f"Aufgabe 47: \n{searched_data_frame['Athlete']}")

    # Aufgabe 48
    medals_grouped_by_country = group_medals_by_country(data, "Switzerland")
    print(f"Aufgabe 48: \n{medals_grouped_by_country.head()}")

    # Aufgabe 49
    # 1. Grafik: USA Balkendiagramm über die Jahre
    # 2. Grafik: Soviet Union Balkendiagramm
    # 3. Grafik: West Germany Balkendiagramm
    # 4. Grafik: East Germany Balkendiagramm
    # 5. Grafik: Count Medals for each Country over ALL Years
    app = aufgabe49(data)
    app.run_server(debug=True, host="0.0.0.0", port=9999)


if __name__ == "__main__":
    main()
