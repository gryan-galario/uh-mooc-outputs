#!/usr/bin/env python3

import pandas as pd

def suicide_fractions():
    df = pd.read_csv("who_suicide_statistics.csv")
    df["Average"] = df["suicides_no"] / df["population"]
    groups = df.groupby("country")
    return groups["Average"].mean()

def suicide_weather():
    fractions = suicide_fractions()
    temp = pd.read_html("List_of_countries_by_average_yearly_temperature.html", index_col = 0, header = 0)
    temp = temp[0]
    col = "Average yearly temperature (1961–1990, degrees Celsius)"
    temp[col] = temp[col].str.replace("\u2212", "-")
    temp[col] = temp[col].map(float)
    common = pd.merge(fractions, temp, left_on = fractions.index, right_on = temp.index)
    corr = common["Average"].corr(common[col], method = "spearman")
    return (fractions.shape[0], temp.shape[0], common.shape[0], corr)

def main():
    a = suicide_weather()
    #print(a)
    print(f"Suicide DataFrame has {a[0]} rows")
    print(f"Temperature DataFrame has {a[1]} rows")
    print(f"Common DataFrame has {a[2]} rows")
    print("Spearman correlation: {:.1f}".format(a[3]))

if __name__ == "__main__":
    main()
