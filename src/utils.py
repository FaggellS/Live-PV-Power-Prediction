import time
import numpy as np

import matplotlib.pyplot as plt
from os.path import dirname, join as pjoin

from datetime import timedelta

from matplotlib.ticker import MaxNLocator


rmse_graph_path = pjoin("..", "output", "graph_rmse.png")
pv_graph_path = pjoin("..","output","graph_pv.png")



def advance_time(timestamp, loop, interval):
        
        timestamp = timestamp + timedelta(minutes = (loop * 10))

        return timestamp



def plot_pv(full_df, sw, ps):

    if len(full_df) <= sw:
        return

    tss = full_df.index
    

    x_label = f"Hours from {tss[0].day:02}.{tss[0].month:02}.{tss[0].year} to {tss[0].day:02}.{tss[0].month:02}.{tss[0].year}"

    times = [f"{ts.day:02}.{ts.month:02}.{ts.year} {ts.hour:01}:{ts.minute:01}" for ts in tss]

    

    scope1 = [f"{ts.day:2}.{ts.month:02} - {ts.hour:02}:{ts.minute:02}" for ts in tss]

    scope2 = [f"{ts.hour:02}:{ts.minute:02}" for ts in tss]

    scope3 = [f"{ts.hour:01}h" for ts in tss]

    
    fig = plt.Figure(figsize=(15, 8), dpi=100)

    ax = fig.add_subplot(111)
    ax.set_title(f"Predicted PV Output Over Time\nWith Sliding window: {sw}, and Pred. interval: {ps * 10}")
    ax.set_xlabel(x_label, labelpad=15)
    ax.set_ylabel("Output (W)", labelpad=15)



    ax.plot(times, full_df["pred_power"], marker='o')
    ax.plot(times, full_df["true_power"], marker='o')

    ax.legend(['Predicted PV power', 'Actual PV power'])

    ax.set_xticklabels(scope1)

    if len(times) > 6:
        ax.set_xticks(range(0, len(times), 6))
        ax.set_xticklabels(scope2[::6])

    if len(times) > 72:
        ax.set_xticks(range(0, len(times), 6))
        ax.set_xticklabels(scope3[::6])


    if len(times) > 144:
        ax.set_xticks(range(0, len(times), 18))
        ax.set_xticklabels(scope3[::18])

    fig.savefig(pv_graph_path)




def plot_rmse(full_df, sw, ps):

    if len(full_df) <= sw:
        return

    tss = full_df.index
    
    x_label = f"Hours from {tss[0].day:02}.{tss[0].month:02}.{tss[0].year} to {tss[0].day:02}.{tss[0].month:02}.{tss[0].year}"

    times = [f"{ts.day:02}.{ts.month:02}.{ts.year} {ts.hour:01}:{ts.minute:01}" for ts in tss]

    scope1 = [f"{ts.day:2}.{ts.month:02} - {ts.hour:02}:{ts.minute:02}" for ts in tss]

    scope2 = [f"{ts.hour:02}:{ts.minute:02}" for ts in tss]

    scope3 = [f"{ts.hour:01}h" for ts in tss]


    fig = plt.Figure(figsize=(15, 8), dpi=100)
    ax = fig.add_subplot(111)
    
    ax.set_title(f"RMSE over time\nWith Sliding window: {sw}, and Pred. interval: {ps * 10}")
    ax.set_xlabel(x_label, labelpad=15)
    ax.set_ylabel("Relative RMSE score", labelpad=15)


    ax.plot(times, full_df["rmse"])

    ax.set_xticklabels(scope1)

    if len(times) > 6:
        ax.set_xticks(range(0, len(times), 6))
        ax.set_xticklabels(scope2[::6])

    if len(times) > 72:
        ax.set_xticks(range(0, len(times), 6))
        ax.set_xticklabels(scope3[::6])


    if len(times) > 144:
        ax.set_xticks(range(0, len(times), 18))
        ax.set_xticklabels(scope3[::18])



    fig.savefig(rmse_graph_path)




def progress_bar_advance(t0, max_time):

    t = time.time() - t0 # elapsed time

    percent = (t * 100) / max_time

    if abs(percent  % 5) < 0.2 or percent == 0 or percent == 100:

        bar = '#' * int(percent)
        empty = ' ' * int(100 - percent)
        st = bar + empty
        print(f"progress: {st}| ({int(percent)}%)", end="\r", flush=True)
    