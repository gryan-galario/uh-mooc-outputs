#!/usr/bin/env python3

import pandas as pd
from sklearn import linear_model

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

def cycling_weather_continues(station):
    weather = pd.read_csv("kumpula-weather-2017.csv")
    biker = split_date_continues()
    biker = biker.drop("Hour", axis = 1)
    biker = biker.groupby(["Year", "Month", "Day"]).sum()
    biker = biker[(2017,1):(2017,12)]
    weather = weather.drop(["Time", "Time zone"], axis = 1)
    weather = weather.rename(columns = {"m": "Month", "d": "Day"})
    weather = weather.set_index(["Year", "Month", "Day"])
    fin = biker.merge(weather, left_index = True, right_index = True)
    fin = fin.ffill()
    model = linear_model.LinearRegression(fit_intercept = True)
    ind = ["Precipitation amount (mm)", "Snow depth (cm)", "Air temperature (degC)"]
    model.fit(fin[ind], fin[station])
    return (tuple(model.coef_), model.score(fin[ind], fin[station]))
    
def main():
    station = "Baana"
    coef, score = cycling_weather_continues(station)
    var = ["'precipitation'", "'snow depth'", "'temperature'"]
    print(f"Measuring station: {station}")
    for i in range(3):
        print(f"Regression coefficient for variable {var[i]}: {coef[i]:.1f}")
    print(f"Score: {score:.2f}")
    return

if __name__ == "__main__":
    main()
