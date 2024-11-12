import matplotlib.colors
import numpy as np
import geopandas as gpd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# %matplotlib notebook
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil, floor
from datetime import datetime
import os
from analysis.common import save_to_directory
from copy import deepcopy
import matplotlib as mpl


def plot_all(ax, df: pd.DataFrame, colorbar:bool, pol:str):
    CONST = size_consts[pol]
    print(CONST)
    print(df.columns)

    """
    temp = df[(df[pol+'_DA_before'] < DA_THRESHOLD_BEFORE_CLEANING)] # Plot hollow red sites less than 75% data availability even BEFORE cleaning
    # print(temp[['site_id', 'site_name', pol+'_DA', pol+'_DA_before']])
    ax.scatter(temp['lon'], temp['lat'], label=None, facecolors='#808080', 
                            edgecolors='#808080', 
                            s=1.5, linewidth=0.25, alpha=1) # Plot all gray sites
    temp = df[(df[pol+'_DA'] < DA_THRESHOLD_AFTER_CLEANING) & (df[pol+'_DA_before'] > DA_THRESHOLD_BEFORE_CLEANING)] # Plot black sites with less than 50% data availability AFTER cleaning
    # print(temp[['site_id', 'site_name', pol+'_DA', pol+'_DA_before']])
    ax.scatter(temp['lon'], temp['lat'], label=None, 
                            edgecolors='#000000', c='#000000',
                            s=1.5, linewidth=0.1, alpha=1) # Plot all gray sites
    """

    temp_da = df[(df[pol+'_DA'] >= DA_THRESHOLD_AFTER_CLEANING) & (df[pol+'_DA_before'] >= DA_THRESHOLD_BEFORE_CLEANING)] # Plot only sites with more than 75% data availability
    temp_da_percentage = temp_da[(temp_da['percentage_change'] > -20) & (temp_da['percentage_change'] < 100)]
    temp_da_percentage = temp_da_percentage[np.logical_not(temp_da_percentage['compliance_change'])]
    
    cmap, cvals, ticks = get_colorbar(pol)
    normalizer = (min(cvals), max(cvals))
    temp_da_percentage = temp_da_percentage.sort_values(by='percentage_change')
    z1_plot = ax.scatter(temp_da_percentage['lon'], temp_da_percentage['lat'], label=None, c=temp_da_percentage['percentage_change'], 
                            cmap=cmap, 
                            vmin = normalizer[0], 
                            vmax = normalizer[1],
                            edgecolors='#707070', 
                            s=temp_da_percentage['pollutant_after_cleaning']*CONST, 
                            linewidth=0.25, alpha=1) 
    if colorbar == True: 
        pol_string = {
            'Ozone':'O' + '$_{3}$',
            'NO2':'NO' + '$_{2}$',
            'PM25':'PM' + '$_{2.5}$',
            'PM10':'PM' + '$_{10}$'
        }
        cbaxes = inset_axes(ax, width="30%", height="3%",loc='lower right',
                            bbox_to_anchor=(-0.13,0.14,1,1), bbox_transform=axs[axes[idx][0], axes[idx][1]].transAxes) 
        cvals = np.array(cvals)

        cbar = plt.colorbar(z1_plot, cbaxes,orientation='horizontal', ticks = ticks, shrink = 1, extend='both', extendfrac=0.1)
        # cbar = plt.colorbar(z1_plot, cbaxes,orientation='horizontal', ticks = cvals, shrink = 1)
        cbar.dividers.set_linewidth(0.4)

        cbaxes.set_title("Change in annual mean "+  pol_string[pol] + ' [%]', fontsize = 5.5)
        cbaxes.tick_params(labelsize=5,width = 0.5)
        cbar.outline.set_linewidth(0.4)
        pol_areas = {
            'Ozone': [5,30,50],
            'NO2': [5,50,80],
            'PM25': [20,50,90],
            'PM10': [20,50,90]
        }
        for area in pol_areas[pol]:
            if area == 0: area = 1
            ax.scatter([], [], c='k', alpha=1, s=area, label = area)
        ax.legend(scatterpoints=1, frameon=False,loc="upper right",
                labelspacing=1, title='Annual mean'+"\n"+
                                        '    [µg m' + '$^{-3}$' + ']',
                prop={'size': 6}, bbox_to_anchor =(0.89, 0.99), ncol = 1).get_title().set_fontsize('6')
    
    temp_compliance = temp_da[temp_da['compliance_change']]
    ax.scatter(temp_compliance['lon'], temp_compliance['lat'], label=None, c=temp_compliance['percentage_change'], 
                            cmap=cmap, 
                            vmax=100,
                            vmin = -20, 
                            edgecolors='black', 
                            s=temp_compliance['pollutant_after_cleaning']*CONST, linewidth=0.5, alpha=1)

