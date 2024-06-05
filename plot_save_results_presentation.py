import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_save_results_presentation(glucose:np.ndarray, insulin_bolus:np.ndarray, i:np.ndarray, m:np.ndarray, time:np.ndarray, plot:bool=False, title:str=None, save:bool=False, save_name:str=None, save_path:str='img') -> None:
    """
    Plot and save the results of the simulation as png for the Power Point presentation.

    Parameters
    ----------
    :param glucose: Vector with the glucose concentration values in mg/dl
    :param insulin_bolus: Vector with the insulin bolus values in U/min
    :param i: Vector with the basal insulin values in U/min
    :param m: Vector with the meal values in g
    :param time: Vector with the datetime values
    :param plot: Boolean to plot the results
    :param title: Title of the plot
    :param save: Boolean to save the plot
    :param save_name: Name of the file to save. Must be provided if save is True
    :param save_path: Path to save the file

    Returns
    -------
    :return: None
    """
    if save and save_name is None:
        raise ValueError("save_name must be provided if save is True")

    # Ensure save_path exists
    if save and not os.path.exists(save_path):
        os.makedirs(save_path)

    xmin = time[0]
    xmax = time[-1]
    linewidth = 2
    text_vspace = 4
    font_size = 8

    fig, ax = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.set_figheight(6)
    fig.set_figwidth(10)

    if title is not None:
        fig.suptitle(title, fontsize=16)

    # Subplot 1: Glucose
    ymin = 50
    ymax = 200
    yub = 180
    ylb = 70
    yss = 120

    ax[0].fill_between(np.array([time[0], time[-1]]), np.array([ylb, ylb]), np.array([yub, yub]), color='green', alpha=0.2)
    ax[0].plot(time, glucose, color='red', linewidth=linewidth)
    ax[0].axhline(y=yub, color='black', linewidth=linewidth, linestyle='--')
    ax[0].axhline(y=yss, color='black', linewidth=1, linestyle='-.')
    ax[0].axhline(y=ylb, color='black', linewidth=linewidth, linestyle='--')
    ax[0].text(time[len(time)//2], yub+text_vspace, 'Hyperglycaemia', fontsize=font_size, fontweight='bold', color='black', ha='center')
    ax[0].text(time[len(time)//2], ylb-2*text_vspace, 'Hypoglycaemia', fontsize=font_size, fontweight='bold', color='black', ha='center')
    ax[0].set_ylabel('Glucose Concentration [mg/dl]')
    ax[0].set_ylim([ymin, ymax])
    ax[0].set_yticks([ylb, yss, yub])
    ax[0].set_xlim([xmin, xmax])
    ax[0].grid()

    # Subplot 2: Meals and Insulin
    imin = 0
    imax = 0.05
    iub = 0.04
    iss = 0.0022

    ax2 = ax[1]
    ax2.plot(time, i, color='blue', linewidth=linewidth)
    ax2.axhline(y=iss, color='black', linewidth=1, linestyle='-.')
    ax2.axhline(y=iub, color='black', linewidth=linewidth, linestyle='--')
    ax2.set_ylabel('Basal Insulin [U/min]')
    ax2.set_ylim([imin, imax])
    ax2.set_yticks([iss, iub])
    ax2.set_xlim([xmin, xmax])
    ax2.grid()

    ax3 = ax2.twinx()

    # Extract unique, non-zero, sorted values of m
    non_zero_m = m[m > 0]
    unique_sorted_m = np.unique(non_zero_m)[::-1] * 5
    yticks_with_zero = np.insert(unique_sorted_m, 0, 0)

    # Mask zero values in m for plotting
    m_non_zero = np.ma.masked_equal(m, 0) * 5
    mmax = max(m) * 5 + 5

    ax3.plot(time, m_non_zero, color='green', linewidth=2)
    ax3.fill_between(time, 0, m_non_zero, color='green', alpha=1.0)
    ax3.set_ylabel('Meal Size [g]', color='green')
    ax3.set_ylim([0, mmax])
    ax3.set_yticks(yticks_with_zero)
    ax3.tick_params(axis='y', labelcolor='green')
    ax3.grid()

    # Set x-axis
    ax2.set_xlabel('Time [h]')
    # Formatting the x-axis to show only hours
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=6)) # Set major ticks to interval hour
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H')) # Format the ticks to show hours

    plt.tight_layout()

    if save:
        # Save the plot to the specified path
        full_save_path = os.path.join(save_path, save_name)
        plt.savefig(full_save_path)
        print(f"Plot saved to {full_save_path}")
    
    if plot:
        plt.show()

    plt.close()