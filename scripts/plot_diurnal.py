'''
Get grouped returns the column with confidence interval with lower and upper bounds
"""
    Plots diurnal curve for pollutant
    Upper and lower boundaries denotes confidence interval (95%)
"""
'''
import pandas as pd
import numpy as np
from copy import deepcopy


def get_grouped(df, col):
    if 'dates' not in df.columns:
        df['dates'] = df['Timestamp']
    df_grouped = (df[[col]].groupby(df['dates'].dt.hour).agg(['mean', 'std', 'count']))
    df_grouped = df_grouped.droplevel(axis=1, level=0).reset_index()
    # Calculate a confidence interval as well.
    df_grouped['ci'] = 1.96 * df_grouped['std'] / np.sqrt(df_grouped['count'])
    df_grouped['ci_lower'] = df_grouped['mean'] - df_grouped['ci']
    df_grouped['ci_upper'] = df_grouped['mean'] + df_grouped['ci']

    return df_grouped

def plot_diurnal(df: pd.DataFrame, color, pollutant, ax):
    if 'dates' not in df.columns:
        df['dates'] = df['Timestamp']
    # ax.legend(loc='upper right')
    # ax.set_ylim(ymin=0)
    df_grouped = (df[[pollutant]].groupby(df['dates'].dt.hour).agg(['mean', 'std', 'count']))
    df_grouped = df_grouped.droplevel(axis=1, level=0).reset_index()
    df_grouped['ci'] = 1.96 * df_grouped['std'] / np.sqrt(df_grouped['count'])
    df_grouped['ci_lower'] = df_grouped['mean'] - df_grouped['ci']
    df_grouped['ci_upper'] = df_grouped['mean'] + df_grouped['ci']

    ymin = round(df_grouped['ci_lower'].min() * 0.9) if (df_grouped['ci_lower'].min()) < ax.get_ylim()[0] else ax.get_ylim()[0]
    ymax = round(df_grouped['ci_upper'].max() * 1.1) if (df_grouped['ci_upper'].max()) > ax.get_ylim()[1] else ax.get_ylim()[1]

    ax.plot(df_grouped['dates'], df_grouped['mean'], color = str(color), label = pollutant)
    ax.fill_between(df_grouped['dates'], df_grouped['ci_lower'], df_grouped['ci_upper'], color = str(color), alpha=.15)

    ax.set_ylim(ymin, ymax)

def get_diurnal(df, pollutant, color, title, ax):
    # df_grouped_NO = get_grouped(df, pollutant)
    plot_diurnal(df, color, pollutant, ax)

