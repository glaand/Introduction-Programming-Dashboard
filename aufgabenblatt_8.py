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
        return pd.read_csv(file)


def getNumRowAndCol(dataFrame) -> Tuple[int, int]:
    return len(dataFrame), len(dataFrame.columns)


if __name__ == "__main__":
    # Exercise 36
    student1, student2 = getAuthors()
    printAuthors()

    # Exercise 37
    df = load_data()
    row, col = getNumRowAndCol(df)
    print(f"{row} Datensätze mit {col} Spalten.")
