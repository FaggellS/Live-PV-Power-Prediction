import tkinter as tk


def update_output_labels(table_labels, output_data):

    table_labels[0]["text"] = output_data["loop"]
    table_labels[1]["text"] = output_data["time"]
    table_labels[2]["text"] = output_data["pred_power"]
    table_labels[3]["text"] = output_data["pred_time"]

    if isinstance(output_data["pred_power"], float):
            table_labels[2]["text"] = f"{output_data["pred_power"]:.2F} (W)"

    if isinstance(output_data["pred_time"], float):
            table_labels[3]["text"] = f"{output_data["pred_time"]:.2F} (s)"

    return table_labels



def initialize_output_labels(output_grid, table_labels):

    for lbl in table_labels:
         lbl.destroy()

    table_labels = []

    for i, txt in enumerate(["Loop:", "Prediction Time:", f"Predicted PV Power:", "Computation Speed:"]):

        lbl1 = tk.Label(output_grid, text = txt, width=20, bg='lightgray', font=("Helvetica", 10, "bold"))
        lbl1.grid(row = i, column=0, padx=10, pady=10)

        lbl2 = tk.Label(output_grid, text="--", bg='gray', font=("Helvetica", 11, "bold"))
        lbl2.grid(row = i, column=1, padx=10, pady = 8)

        table_labels.append(lbl2)

    

    return output_grid, table_labels



def define_output_frame(output_frame):

    tk.Label(output_frame, text="Model Output:", font=("Helvetica", 14, "bold"), bg="lightgray", borderwidth=2).pack(side="top", fill="x")

    output_grid = tk.Frame(output_frame, background="gray", highlightbackground="black", highlightthickness=0.5, borderwidth=10)
    output_grid.pack(pady=40, padx=10, fill="both", expand=True)

    # font=("Helvetica", 12)

    output_grid.columnconfigure(0, weight=1)
    output_grid.columnconfigure(1, weight=2)

    output_grid, output_table_labels = initialize_output_labels(output_grid, [])

    
    return output_frame, output_grid, output_table_labels



