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


# =============================================================================
# Aufgabe 41
# =============================================================================
def load_data(path=None) -> pd.DataFrame:
    # Data is loaded from GitHub Repo
    if path is None:
        path = "https://raw.githubusercontent.com/glaand/Introduction-Programming-Dashboard/main/datasets/data.csv"
    return pd.read_csv(path).dropna()


def getSortedListByColumnName(df: pd.DataFrame, columnName: str) -> list:
    return sorted(list(df[columnName].unique()))


def aufgabe41():
    df = load_data()
    laender = getSortedListByColumnName(df, "Country")
    gewinner = getSortedListByColumnName(df, "Athlete")
    sportarten = getSortedListByColumnName(df, "Discipline")
    print(f"{laender=}\n{gewinner=}\n{sportarten=}\n")
    print(f"Es gibt {len(laender)} Länder. \nEs gibt {len(gewinner)} Medaillengewinner. \nEs gibt {len(sportarten)} Disziplinen.")


def aufgabe42():
    df = load_data()
    countriesMedalSum = df.groupby(["Country"]).size().reset_index(name='count')
    countriesMedalSum = countriesMedalSum.sort_values(by=["count"], ascending=False)
    print(countriesMedalSum.head(10))


def aufgabe43():
    pass


def aufgabe44():
    pass


def aufgabe45():
    pass


def main():
    # aufgabe41()
    aufgabe42()
    aufgabe43()
    aufgabe44()
    aufgabe45()


if __name__ == "__main__":
    main()
