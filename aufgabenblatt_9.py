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
import os

# =============================================================================
# Constants
# =============================================================================
DATA_PATH = os.path.join("datasets", "data.csv")


# =============================================================================
# Aufgabe 41
# =============================================================================
def load_data(path=None) -> pd.DataFrame:
    if path is None:
        path = DATA_PATH
    with open(path) as file:
        return pd.read_csv(file).dropna()


def getCountries(df) -> list:
    result = list(df["Country"].unique())
    return sorted(result)


def getWinners(df) -> list:
    result = list(df["Athlete"].unique())
    return sorted(result)


def getDiciplines(df) -> list:
    result = list(df["Discipline"].unique())
    return sorted(result)


def aufgabe41():
    df = load_data()
    laender = getCountries(df)
    gewinner = getWinners(df)
    sportarten = getDiciplines(df)
    print(f"{laender=}\n{gewinner=}\n{sportarten=}\n")


def aufgabe42():
    pass


def aufgabe43():
    pass


def aufgabe44():
    pass


def aufgabe45():
    pass


def main():
    aufgabe41()
    aufgabe42()
    aufgabe43()
    aufgabe44()
    aufgabe45()


if __name__ == "__main__":
    main()
