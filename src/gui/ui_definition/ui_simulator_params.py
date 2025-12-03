import tkinter as tk
from tkinter import ttk




def define_buttons(button_frame, startButtonCommand, stopButtonCommand):

    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    start = tk.Button(button_frame, text="Run Experiment", font=("Helvetica", 10, "bold"), bg='gainsboro', command=startButtonCommand)
    stop = tk.Button(button_frame, text="Stop Experiment", font=("Helvetica", 10, "bold"), bg='gainsboro', command=stopButtonCommand)

    start.grid(row=0, column=0, sticky="e", padx=30)
    stop.grid(row=0, column=1, sticky="w", padx=30)

    return button_frame, start, stop


def define_parameter_frame(param_frame, interval_values, sliding_values, ahead_values):

    

    tk.Label(param_frame, text="Simulation Parameters:", bg="lightgray", borderwidth=20, font=("Helvetica", 14, "bold"), highlightbackground="black", highlightthickness=0.5 ).pack(pady = 10)

    ## 0 - demo mode

    frm = tk.Frame(param_frame, borderwidth=10, bg="gray" )

    tk.Label(frm, text="Activate Demo Mode:", bg="gray", font=("Helvetica", 12, "bold")).grid(row=0, column=0)

    demo_mode = tk.IntVar()
    demo_cb = tk.Checkbutton(frm, variable=demo_mode, onvalue=True, offvalue=False, bg="gray")
    
    demo_cb.grid(row=0, column=1, padx=10)

    frm.pack(padx=40, pady=10, anchor="nw", fill=tk.X)

    ## X - Online Retraining

    frm = tk.Frame(param_frame, borderwidth=10, bg="gray" )

    tk.Label(frm, text="Activate Online Retraining:", bg="gray", font=("Helvetica", 12, "bold")).grid(row=0, column=0)

    retrain = tk.IntVar()
    retrain_b = tk.Checkbutton(frm, variable=retrain, onvalue=True, offvalue=False, bg="gray")
    
    retrain_b.grid(row=0, column=1, padx=10)

    frm.pack(padx=40, pady=10, anchor="nw", fill=tk.X)

    ## 1 - prediction interval

    tk.Label(param_frame, text="Prediction Interval:", bg="gray", borderwidth=15, font=("Helvetica", 12, "bold")).pack(padx=40, anchor="nw")
        
    cb1_n = tk.StringVar()
    interval_cb = ttk.Combobox(param_frame, height=0, font=("Helvetica", 11), textvariable=cb1_n)
    
    interval_cb['state'] = 'readonly'
    interval_cb['values'] = [f"Every {ph} minute(s)" for ph in interval_values]

    interval_cb.pack(padx=40, anchor="nw", fill=tk.X)
    interval_cb.set(f"Every {interval_values[-2]} minute(s)")
    
    ## 2 - sliding window

    tk.Label(param_frame, text= "LSTM Sliding Window:", bg="gray", borderwidth=15, font=("Helvetica", 12, "bold")).pack(padx=40, anchor="nw")

    cb2_n = tk.StringVar()
    sliding_cb = ttk.Combobox(param_frame, height=0, font=("Helvetica", 11), textvariable=cb2_n)

    sliding_cb['state'] = 'readonly'
    sliding_cb['values'] = [f"{sw} last recorded values" for sw in sliding_values]

    sliding_cb.pack(padx=40, anchor="nw", fill=tk.X)
    sliding_cb.set(f"{sliding_values[0]} last recorded values")

    
    ## 3 - prediction horizon

    tk.Label(param_frame, text= "LSTM Prediction Horizon:", bg="gray", borderwidth=15, font=("Helvetica", 12, "bold")).pack(padx=40, anchor="nw")

    cb3_n = tk.StringVar()
    ahead_cb = ttk.Combobox(param_frame, height=0, font=("Helvetica", 11), textvariable=cb3_n)

    ahead_cb['state'] = 'readonly'
    ahead_cb['values'] = [f"{av} minutes ahead" for av in ahead_values]

    ahead_cb.pack(padx=40, anchor="nw", fill=tk.X)
    ahead_cb.set(f"{ahead_values[0]} minutes ahead")


    
    

    return demo_mode, retrain, interval_cb, sliding_cb, ahead_cb,  cb1_n, cb2_n, cb3_n
