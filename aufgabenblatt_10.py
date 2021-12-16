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


def filter_data(df: pd.DataFrame, land: str, jahr: int, sportart: str) -> pd.DataFrame:
    if land is not None:
        df = df[df["Country"] == land]
    if jahr is not None:
        df = df[df["Year"] == jahr]
    if sportart is not None:
        df = df[df["Discipline"] == sportart]
    return df

def group_medals_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    df = filter_data(df, country, None, None)
    return df

if __name__ == "__main__":
    data = load_data()
    # Aufgabe 46
    # result_data_frame = filter_data(data, "Schweiz", 2008, "Swimming")

    # Aufgabe 48
    medals_grouped_by_country = group_medals_by_country(data, "Switzerland")
    print(medals_grouped_by_country)