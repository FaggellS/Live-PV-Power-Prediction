import tkinter as tk

from datetime import timedelta

import time


def start_timer(root, label, tmax):
    tmax = tmax * 60
    t0 = time.time() 


    def update_timer():
        nonlocal t0
        duration = time.time() - t0  
        remaining_time = max(tmax - int(duration), 0) 
        
        label.configure(text=f"Next prediction in: {int(remaining_time)}s")
        
        if remaining_time > 0:
            root.after(1000, update_timer)  
        else:
            label.configure(text="Next prediction in: --")

    update_timer()  



def update_status(status, is_on):

    if is_on:
        status.config(text="SIMULATION ON", background="green")
    else:
        status.config(text="SIMULATION OFF", background="red3")
    
    return status

def update_time(start_lbl, finish_lbl, start_ts, finish_ts):

    start_str = "--"
    finish_str = "--"


    if not isinstance(start_ts, str):

        start_str = f"{start_ts.day:02}.{start_ts.month:02} - {start_ts.hour:02}:{start_ts.minute:02}:{start_ts.second:02}"

    if not isinstance(finish_ts, str):

        finish_str = f"{finish_ts.day:02}.{finish_ts.month:02} - {finish_ts.hour:02}:{finish_ts.minute:02}:{finish_ts.second:02}"


    start_lbl.config(text= f"Simulation Start: {start_str}")
    finish_lbl.config(text= f"Simulation End: {finish_str}")

    return start_lbl, finish_lbl

def update_rmse(rmse_lbl, rmse_l):


    score = rmse_l

    if isinstance(rmse_l, list):
        if len(rmse_l) == 0:

            score = 0.0
        else:
            score = rmse_l[-1]
    
    rmse_lbl.config(text=f"Current RMSE score: {score:.2f}")

    return rmse_lbl

def define_misc(top_bar, bottom_bar):

    status = tk.Label(top_bar, text="SIMULATION OFF", width=15, font=("Helvetica", 7, "bold"), fg="white", background="red3", highlightthickness=0.5, highlightcolor="black", borderwidth=5)
    status.pack(side="right", padx=15, pady=10)

    start_time = tk.Label(bottom_bar, background="lightgray", text="Simulation Start: --", font = ("Helvetica", 12) )

    finish_time = tk.Label(bottom_bar, background="lightgray", text="Simulation End: --", font = ("Helvetica", 12))

    start_time.pack(side="left", pady=20, padx=30, fill="both")
    finish_time.pack(side="right", pady=20, padx=30, fill="both")


    middle_label = tk.Label(bottom_bar,  background="lightgray", text="Next prediction in: --", font = ("Helvetica", 12) )
    middle_label.pack(pady=20, fill="both" )

    return status, start_time, finish_time, middle_label