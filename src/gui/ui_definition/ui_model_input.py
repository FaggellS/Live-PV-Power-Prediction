import tkinter as tk
import numpy as np


def update_input_labels(table_labels, list_of_dict):

    for labels in table_labels[1:]:
        for lbl in labels:
            lbl.config(text="--")

    for i, row in enumerate(list_of_dict):

        row_index = i+1

        table_labels[row_index][0]["text"] = row["timestamp"]
        table_labels[row_index][1]["text"] = row["irradiance"]
        table_labels[row_index][2]["text"] = row["temperature"]
        table_labels[row_index][3]["text"] = row["true_power"]

        if isinstance(row["true_power"], float):
            table_labels[row_index][3]["text"] = f"{row["true_power"]:.2F}"

    return table_labels



def initialize_input_labels(input_table, table_labels, sliding_window):

    table_labels = delete_input_labels(table_labels)

    for j in range(sliding_window):

        jdx = j+1

        row_labels = []

        for i in range(4):

            lbl = tk.Label(input_table, text = "--", width=20, bg='lightgray', font=("Helvetica", 9))

            if j ==  ( sliding_window - 1 ):
                lbl.config(background="plum3")

            lbl.grid(row=jdx, column=i, padx=10, pady=5)

            row_labels.append(lbl)

        table_labels.append(row_labels)
    
    return input_table, table_labels





def delete_input_labels( table_labels):

    for labels in table_labels[1:]:
        for lbl in labels:
            lbl.destroy()

    return [table_labels[0]]



def initialize_column_labels(input_table):

    table_labels = []
    row_labels = []

    for i, txt in enumerate(["Time", f"Irradiance (W/m\u00B2)", f"Temperature (\u00B0C)", "PV Power (W)"]):

        lbl = tk.Label(input_table, text = txt, width=20, bg='lightgray', font=("Helvetica", 10, "bold"))
        lbl.grid(row=0, column=i, padx=10, pady=10)

        row_labels.append(lbl)

    table_labels.append([*row_labels])


    return input_table, table_labels



def define_input_frame(input_frame):

    tk.Label(input_frame, text="Model Input:", bg='lightgray', font=("Helvetica", 14, "bold"), borderwidth=10 ).pack(anchor="c", side="top", fill="x")

    # input grid

    input_table_wrapper = tk.Frame(input_frame, background="gray", highlightbackground="black", highlightthickness=0.5, borderwidth=10)
    input_table_wrapper.pack(pady=10, padx=10, fill="both", expand=True)

    input_table = tk.Frame(input_table_wrapper, bg="gray20", highlightbackground="black", highlightthickness=0.5, borderwidth=10)
    input_table.pack(fill="both", expand=True)

    # base grid configuration - we will change it when simulation starts

    input_table, table_labels = initialize_column_labels(input_table)

    return input_frame, input_table, table_labels






