import tkinter as tk



def build_root():

    root = tk.Tk()
    root.title("Live PV Prediction - Simulation Framework")
    root.geometry("1200x780")

    return root


def build_root_layout(root):

    ## top and bottom bars

    top_bar = tk.Frame(root, background="gray60", height=40)
    bottom_bar = tk.Frame(root, bg='lightgray', highlightbackground="black", highlightthickness=0.5, height=80)

    top_bar.pack(side="top", fill="x")
    bottom_bar.pack(side="bottom", fill="x")

    ## main frame

    main = tk.Frame(root, background="gray25")

    main.columnconfigure(0, weight=3, minsize=250)
    main.columnconfigure(1, weight=5)
    main.rowconfigure(0, weight=1)

    main.pack(side="top", fill="both", expand=True)

    return top_bar, main, bottom_bar



def main_frame_layout(main):

    ## main frame separation

    left_frame = tk.Frame(main, background='lightgray')
    right_frame = tk.Frame (main, background="gray25")

    left_frame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
    right_frame.grid(row=0, column=1, sticky="NSEW", padx=10, pady=10)

    return left_frame, right_frame

def right_frame_layout(right_frame):

    ## right frame grid

    right_frame.rowconfigure(0, weight=1)
    right_frame.rowconfigure(1, weight=1, minsize = 50)
    right_frame.columnconfigure(0,weight=1)

    ## right frame separation

    input_frame = tk.Frame (right_frame, bg='lightgray', highlightbackground="black", highlightthickness=0.5)
    input_frame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
    
    output_frame = tk.Frame (right_frame, background='lightgray', highlightbackground="black", highlightthickness=0.5, borderwidth=10)
    output_frame.grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

    return right_frame, input_frame, output_frame

def left_frame_layout(left_frame):

    param_frame = tk.Frame(left_frame,  bg='gray', highlightbackground="black", highlightthickness=0.5)
    button_frame = tk.Frame(left_frame, bg='lightgray')

    param_frame.pack(side="top", fill="both",padx=10, pady=10, anchor="n", expand=True)
    button_frame.pack(pady=20, fill="x")

    return param_frame, button_frame