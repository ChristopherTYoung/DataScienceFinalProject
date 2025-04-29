import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def avg_per_color(df):
    avg_per_color = df.groupby("color_identity")["pick_number"].mean()
    avg_per_color.plot(kind='bar', title='Avg Pick # by Color')
    plt.show()