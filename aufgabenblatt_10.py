#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : André Glatzl
# Credits     : Alexandru Schneider
# Created Date: 16. 12. 2021
# =============================================================================
"""Aufgabenblatt 8"""


# =============================================================================
# Imports
# =============================================================================
from traitlets.traitlets import default
from aufgabenblatt_9 import load_data
import pandas as pd


def filter_data(df: pd.DataFrame, land: str, jahr: int, sportart: str) -> pd.DataFrame:
    if land is not None:
        df = df[df["Country"] == land]
    if jahr is not None:
        df = df[df["Year"] == jahr]
    if sportart is not None:
        df = df[df["Discipline"] == sportart]
    return df

def filter_data2(df: pd.DataFrame, string: str) -> pd.DataFrame:
    df = df[df["Athlete"].str.contains(string)]
    return df

def group_medals_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    df = filter_data(df, country, None, None)
    df = df.groupby(["Country", "Medal"]).size().reset_index(name="Count")
    df = df.drop("Country", axis=1).set_index("Medal").transpose()
    return df


if __name__ == "__main__":
    data = load_data()
    # Aufgabe 46
    # result_data_frame = filter_data(data, "Switzerland", 2008, "Swimming")

    # Aufgabe 47
    # searched_data_frame = filter_data2(data, "Ale")

    # Aufgabe 48
    medals_grouped_by_country = group_medals_by_country(data, "Switzerland")
    print(medals_grouped_by_country)