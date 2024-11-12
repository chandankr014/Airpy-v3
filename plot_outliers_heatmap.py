import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib


def plot_outlier_heatmap(monthly_condensed_summary: str, savefile: str):
    pols = ['NO', 'NO2', 'NOx', 'Ozone', 'PM10', 'PM25']
    net = pd.read_csv(monthly_condensed_summary)
    melts = pd.DataFrame(columns=['year','month','pol','repeats'])
    
    for pol in pols:
        net[pol] = (net[pol + '_consecutives'] - net[pol + '_outliers']) / net[pol + '_consecutives'] * 100
        # temp = net.groupby(['year','month'])
        temp = net.melt(id_vars=['year','month'], value_vars=[pol], var_name='pol', value_name='repeats')
        melts = pd.concat([melts, temp], axis=0)
    
    print(melts)
    net = melts

    # Fill NaN values with 0 for the 'repeats' column
    net['repeats'] = net['repeats'].fillna(0)

    matplotlib.rcParams.update({'font.size': 11, "font.family": "Arial"})
    matplotlib.rcParams['legend.handlelength'] = 1
    matplotlib.rcParams['legend.handleheight'] = 1
    params = {'mathtext.default': 'regular'}
    sns.set_style({'font.family': 'sans-serif', 'font.serif': 'Arial', 'font.size': 11})
    plt.rcParams.update(params)

    f, (ax1, ax2, ax3, ax4, ax5, axcb) = plt.subplots(1, 6, figsize=(25, 3),
                                                      gridspec_kw={'width_ratios': [1, 1, 1, 1, 1, 0.08]})

    net1 = net[(net['year'] == 2019)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g1 = sns.heatmap(heatmap_data, cmap="jet", cbar=False, ax=ax1, annot=True, fmt='.1f', annot_kws={"fontsize": 7.7})
    g1.set_ylabel('Pollutant')
    g1.set_xlabel('')

    net1 = net[(net['year'] == 2020)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g2 = sns.heatmap(heatmap_data, cmap="jet", cbar=False, ax=ax2, annot=True, fmt='.1f', annot_kws={"fontsize": 7.5})
    g2.set_ylabel('')
    g2.set_xlabel('')
    g2.set_yticks([])

    net1 = net[(net['year'] == 2021)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g3 = sns.heatmap(heatmap_data, cmap="jet", cbar=False, ax=ax3, annot=True, fmt='.1f', annot_kws={"fontsize": 7.5})
    g3.set_ylabel('')
    g3.set_xlabel('')
    g3.set_yticks([])

    net1 = net[(net['year'] == 2022)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g4 = sns.heatmap(heatmap_data, cmap="jet", cbar=False, ax=ax4, annot=True, fmt='.1f', annot_kws={"fontsize": 7.5})
    g4.set_ylabel('')
    g4.set_xlabel('')
    g4.set_yticks([])

    net1 = net[(net['year'] == 2023)]
    heatmap_data = pd.pivot_table(net1, values='repeats', index=['pol'], columns='month')
    g5 = sns.heatmap(heatmap_data, cmap="jet", ax=ax5, cbar_ax=axcb, annot=True, fmt='.1f', annot_kws={"fontsize": 7.5}, cbar_kws={'label': 'Outliers [%]'})
    g5.set_xlabel('')
    g5.set_ylabel('')
    g5.set_yticks([])

    # Rotate the ticklabels
    for ax in [g1, g2, g3, g4, g5]:
        tl = ax.get_xticklabels()
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
        tly = ax.get_yticklabels()
        ax.set_yticklabels(tly, rotation=0)

    # Set titles and other text
    ax1.set_title("2019")
    ax2.set_title("2020")
    ax3.set_title('2021')
    ax4.set_title('2022')
    ax5.set_title('2023')
    g2.set_xlabel('Months')
    g1.set_yticklabels(["NO", "NO" + '$_{2}$', "NO" + '$_{x}$', "O" + '$_{3}$', "PM" + '$_{10}$', "PM" + '$_{2.5}$'])

    plt.text(.005, 1.09, ' (f)', ha='left', va='top', transform=ax1.transAxes, size=11, backgroundcolor='none')
    plt.text(.005, 1.09, ' (g)', ha='left', va='top', transform=ax2.transAxes, size=11, backgroundcolor='none')
    plt.text(.005, 1.09, ' (h)', ha='left', va='top', transform=ax3.transAxes, size=11, backgroundcolor='none')
    plt.text(.005, 1.09, ' (i)', ha='left', va='top', transform=ax4.transAxes, size=11, backgroundcolor='none')
    plt.text(.005, 1.09, ' (j)', ha='left', va='top', transform=ax5.transAxes, size=11, backgroundcolor='none')

    f.savefig(savefile, dpi=1200, bbox_inches="tight")


def plot_consecutives_heatmap(monthly_condensed_summary: str, savefile: str):
    pols = ['NO', 'NO2', 'NOx', 'Ozone', 'PM10', 'PM25']
    net = pd.read_csv(monthly_condensed_summary)
    melts = pd.DataFrame(columns=['year', 'month', 'pol', 'repeats'])
    
    # Loop through each pollutant and calculate repeats percentage
    for pol in pols:
        # Calculate the repeats percentage and fill NaN values with 0
        net[pol] = ((net[pol] - net[pol + '_consecutives']) / net[pol]) * 100
        net[pol] = net[pol].fillna(0)  # Fill NaN with 0, or use other strategy if needed
        temp = net.melt(id_vars=['year', 'month'], value_vars=[pol], var_name='pol', value_name='repeats')
        melts = pd.concat([melts, temp], axis=0)
    
    net = melts

    # Setting plot parameters and styles
    matplotlib.rcParams.update({'font.size': 11, "font.family": "Arial"})
    matplotlib.rcParams['legend.handlelength'] = 1
    matplotlib.rcParams['legend.handleheight'] = 1
    params = {'mathtext.default': 'regular'}
    sns.set_style({'font.family': 'sans-serif', 'font.serif': 'Arial', 'font.size': 11})
    plt.rcParams.update(params)

    # Create subplots for each year
    f, (ax1, ax2, ax3, ax4, ax5, axcb) = plt.subplots(1, 6, figsize=(25, 3),
                                                     gridspec_kw={'width_ratios': [1, 1, 1, 1, 1, 0.08]})

    # Plot each year's data
    for i, (year, ax) in enumerate(zip(range(2019, 2024), [ax1, ax2, ax3, ax4, ax5])):
        net_year = net[net['year'] == year]
        heatmap_data = pd.pivot_table(net_year, values='repeats', index='pol', columns='month')
        sns.heatmap(heatmap_data, cmap="jet", cbar=(ax == ax5), ax=ax, annot=True, fmt='.1f',
                    annot_kws={"fontsize": 7.5}, cbar_ax=axcb if ax == ax5 else None,
                    cbar_kws={'label': 'Similar Repeats [%]'})
        
        ax.set_title(str(year))
        ax.set_xlabel('')
        if ax != ax1:
            ax.set_yticks([])  # Hide y-ticks for all but the first plot
        else:
            ax.set_ylabel('Pollutant')
        
        # Set month names as x-tick labels
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    
    # Set pollutant labels with subscripts
    ax1.set_yticklabels(["NO", "NO" + '$_{2}$', "NO" + '$_{x}$', "O" + '$_{3}$', "PM" + '$_{10}$', "PM" + '$_{2.5}$'])

    # Set subplot labels
    subplot_labels = ['(a)', '(b)', '(c)', '(d)', '(e)']
    for ax, label in zip([ax1, ax2, ax3, ax4, ax5], subplot_labels):
        plt.text(.005, 1.09, label, ha='left', va='top', transform=ax.transAxes, size=11, backgroundcolor='none')

    # Save the figure
    f.savefig(savefile, dpi=1200, bbox_inches="tight")



# calling
if __name__ == '__main__':
    fn = "files/monthly_condensed_new.csv"
    plot_outlier_heatmap(fn, 'plots/heatmaps/heatmap_outliers_monthly.png')
    plot_consecutives_heatmap(fn, 'plots/heatmaps/heatmap_consecutives_monthly.png')