import tkinter as tk


def update_output_labels(table_labels, output_data):

    
    if len(output_data["rmse"]) == 0:

            score = 0.0
    else:
            score = output_data["rmse"][-1]

    table_labels[0][0]["text"] = output_data["time_t"]
    table_labels[1][0]["text"] = output_data["pred_t"]
    table_labels[2][0]["text"] = output_data["true_t"]
    table_labels[3][0]["text"] = score


    table_labels[0][1]["text"] = output_data["time_tplus"]
    table_labels[1][1]["text"] = output_data["pred_tplus"]
    table_labels[2][1]["text"] = output_data["speed"]



    if isinstance(output_data["pred_t"], float):
        if output_data["pred_t"] == -1:
             table_labels[1][0]["text"] = "--"
        else:
            table_labels[1][0]["text"] = f"{output_data["pred_t"]:.2F} (W)"
    
    if isinstance(output_data["true_t"], float):
        if output_data["true_t"] == -1:
             table_labels[2][0]["text"] = "--"
        else:
            table_labels[2][0]["text"] = f"{output_data["true_t"]:.2F} (W)"

    if isinstance(output_data["pred_tplus"], float):
        table_labels[1][1]["text"] = f"{output_data["pred_tplus"]:.2F} (W)"

    if isinstance(output_data["speed"], float):
            table_labels[2][1]["text"] = f"{output_data["speed"]:.2F} (s)"

    if isinstance(score, float):
            table_labels[3][0]["text"] = f"{score:.2F}"

    return table_labels



def initialize_output_labels(output_grid, table_labels):

    for labels in table_labels:
        for lbl in labels:
            lbl.destroy()

    table_labels = []

    left_text = ["Current Time:", "Pred. PV (Current):", "Real PV:", "Relative RMSE score:"]
    right_text = ["Prediction Time:", "Pred. PV (Future):", "Computation Time:", ""]

    for i in range (4):


        lbl0 = tk.Label(output_grid, text = left_text[i], width=20, bg='lightgray', font=("Helvetica", 10, "bold"))
        lbl0.grid(row = i, column=0, padx=10, pady=10)

        lbl1 = tk.Label(output_grid, text="--", bg='gray', font=("Helvetica", 11, "bold"))
        lbl1.grid(row = i, column=1, padx=10, pady = 8)

        lbl2 = tk.Label(output_grid, text = right_text[i], width=20, bg='lightgray', font=("Helvetica", 10, "bold"))
        lbl3 = tk.Label(output_grid, text="--", bg='gray', font=("Helvetica", 11, "bold"))

        if i == 3:
             lbl3.config(text="", bg= "gray")
             lbl2.config(text="", bg= "gray")

       
        lbl2.grid(row = i, column=2, padx=10, pady=10)
        lbl3.grid(row = i, column=3, padx=10, pady = 8)



        table_labels.append([lbl1, lbl3])

    

    return output_grid, table_labels



def define_output_frame(output_frame):

    tk.Label(output_frame, text="Model Output:", font=("Helvetica", 14, "bold"), bg="lightgray", borderwidth=2).pack(side="top", fill="x")

    output_grid = tk.Frame(output_frame, background="gray", highlightbackground="black", highlightthickness=0.5, borderwidth=10)
    output_grid.pack(pady=40, padx=10, fill="both", expand=True)

    # font=("Helvetica", 12)

    output_grid.columnconfigure(0, weight=1)
    output_grid.columnconfigure(1, weight=2)
    output_grid.columnconfigure(2, weight=1)
    output_grid.columnconfigure(3, weight=2)

    output_grid, output_table_labels = initialize_output_labels(output_grid, [])

    
    return output_frame, output_grid, output_table_labels



