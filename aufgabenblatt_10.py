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
from aufgabenblatt_9 import load_data
import pandas as pd
import re


def filter_data(df: pd.DataFrame, land: str, jahr: int, sportart: str) -> pd.DataFrame:
    if land is not None:
        df = df[df["Country"] == land]
    if jahr is not None:
        df = df[df["Year"] == jahr]
    if sportart is not None:
        df = df[df["Sport"] == sportart]
    return df


def group_medals_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    df = filter_data(df, country, None, None)
    return df


def filter_data2(df, string: str):
    pattern = ""
    for char in string:
        pattern += f"(?=.*{str(char)})"
    pattern += ".*"
    return df[df["Athlete"].str.match(pattern)]


if __name__ == "__main__":
    # load data from csv as dataframe
    data = load_data()
    # change Year column to integer
    data["Year"] = data["Year"].astype(int)

    # Aufgabe 46
    result_data_frame = filter_data(data, "Switzerland", 2008, "Cycling")
    #print(f"Aufgabe 46: \n{result_data_frame.head()}")

    # Aufgabe 47
    searched_data_frame = filter_data2(data, "zv")
    print(f"Aufgabe 47: \n{searched_data_frame['Athlete']}")

    # Aufgabe 48
    medals_grouped_by_country = group_medals_by_country(data, "Switzerland")
    #print(f"Aufgabe 48: \n{medals_grouped_by_country.head()}")
