import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def avg_per_color(df):
    avg_per_color = df.groupby("color_identity")["pick_number"].mean()
    avg_per_color.plot(kind='bar', title='Avg Pick # by Color')
    plt.show()

def win_rate_vs_ata(card_data):
    sns.scatterplot(x="GD WR", y="ATA", data=card_data, hue="color_identity")
    plt.show()

def win_rate_per_color(card_data):
    avg_per_color = card_data.groupby("color_identity")["GD WR"].mean()
    avg_per_color.plot(kind="bar")
    plt.show()