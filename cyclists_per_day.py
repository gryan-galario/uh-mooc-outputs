#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def split_date(df):
    d = df["Päivämäärä"].str.split(expand=True)
    d.columns = ["Weekday", "Day", "Month", "Year", "Hour"]

    hourmin = d["Hour"].str.split(":", expand=True)
    d["Hour"] = hourmin.iloc[:, 0]

    days = dict(zip(["ma", "ti", "ke", "to", "pe", "la", "su"],["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))
    months = dict(zip(["tammi", "helmi", "maalis", "huhti", "touko", "kesä", "heinä", "elo", "syys", "loka", "marras", "joulu"], [i for i in range(1,13)]))

    d["Weekday"] = d["Weekday"].map(days)
    d["Month"] = d["Month"].map(months)
    
    d = d.astype({"Weekday": object, "Day": int, "Month": int, "Year": int, "Hour": int})
    return d

def split_date_continues():
    df = pd.read_csv("Helsingin_pyorailijamaarat.csv", sep = ";")
    df = df.dropna(how = "all")
    df = df.dropna(axis = 1, how = "all")
    return pd.concat([split_date(df), df.drop(["Päivämäärä"], axis = 1)], axis = 1)

def cyclists_per_day():
    df = split_date_continues()
    df = df.drop(["Weekday", "Hour"], axis = 1)
    groups = df.groupby(["Year", "Month", "Day"])
    return groups.sum()
    
    
def main():
    df = cyclists_per_day()
    pts = df.loc[2017, 8]
    plt.plot(pts)
    plt.title('Cyclist Per Day (August 2017)')
    plt.xticks(df.loc[2017,8].index)
    plt.legend(df.columns)
    plt.show()

if __name__ == "__main__":
    main()