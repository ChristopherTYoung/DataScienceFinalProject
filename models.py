import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from has_wheeled import has_wheeled
import statsmodels.api as sm

def avg_per_color(df):
    avg_per_color = df.groupby("color_identity")["pick_number"].mean()
    avg_per_color.plot(kind='bar', title='Avg Pick # by Color')
    plt.xlabel("Color Identity")
    plt.ylabel("Avg Pick #")
    plt.show()

def win_rate_vs_ata(card_data):
    sns.scatterplot(x="GD WR", 
                    y="ATA", 
                    data=card_data, 
                    hue="rarity")
    plt.xlabel("Games Drawn Win Rate")
    plt.ylabel("Avg Pick #")
    plt.title("Avg pick vs Win Rate")
    plt.show()

def win_rate_per_color(card_data):
    avg_per_color = card_data.groupby("color_identity")["GD WR"].mean()
    avg_per_color.plot(kind="bar")
    plt.xlabel("Color Identity")
    plt.ylabel("Avg Win Rate")
    plt.show()

def ata_vs_mana_cost(card_data):
    sns.barplot(x="mana_cost", y="ATA", data=card_data, hue="color_identity")
    plt.xlabel("Mana Cost")
    plt.ylabel("Avg Pick #")
    plt.show()

def gns_vs_ata(card_data):
    sns.scatterplot(x="# GNS", y="ATA", data=card_data, hue="rarity")
    plt.xlabel("Games Not Seen")
    plt.ylabel("Avg Pick #")
    plt.show()

def logistic_regression_model(df, variables):
    df = df.dropna(subset=["has_wheeled"]+variables)
    X = df[variables].apply(pd.to_numeric, errors='coerce')
    X = sm.add_constant(X)
    y = pd.to_numeric(df["has_wheeled"])
    model = sm.Logit(y, X)
    result = model.fit()
    return result