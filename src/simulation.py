from data_storage.storage_manager import Storage

from data_processing.normalize import normalize_list, denormalize_pred
from data_processing.format import format_for_model, prepare_input

from model.model import MatlabLSTM
from model.load_weights import load_matlab_weights
from model.predict import predict_from_sequence

from utils import progress_bar_advance, plot_pv, plot_rmse, advance_time

from threading import Event

from time import time
from datetime import datetime, timedelta

class Simulator:

    def __init__(self):
        
        print("Initialize Simulator")

        self.storage = Storage()

        self.model = MatlabLSTM()
        self.model = load_matlab_weights( self.model )

        self.stop_event = Event()

        self.gui_update = None

        self.demo_start_time = datetime(2024, 9, 6, 5, 0, 0)
        self.demo_end_time = datetime(2024, 9, 8, 5, 0, 0)
        self.demo_mode = False


    # gui callback
    def set_callback(self, callback):

        self.gui_update = callback

    # thread stop
    def stop(self):

        if (not self.stop_event.is_set()):
            self.stop_event.set()
            print("\nStop requested.\n")

        output_dict = {
            "time_t":None, 
            "time_tplus":None, 
            "rmse": None,
            "input_data":None,
            "output_data":None
        }

        self.gui_update(output_dict)





    ## what we call when starting simulation
    def run(self, is_demo_mode, pred_interval, sliding_window, pred_horizon, max_loop = 0):

        
        self.demo_mode = is_demo_mode

        self.sliding_window = sliding_window
        self.pred_interval = pred_interval
        self.pred_step = int( pred_horizon / 10 )

        print(f"simulation started with the following parameters: demo mode: {self.demo_mode}, pred_interval: {pred_interval}, sliding window: {sliding_window}, pred horizon: {self.pred_step}")

        self.stop_event.clear()

        self.loop = 0

        no_loop_limit = False
        if max_loop == 0:
            no_loop_limit = True
        

        

        if self.demo_mode:

            self.start_time = self.demo_start_time

        else:

            ts = datetime.now()
            self.start_time = ts.replace(microsecond=0)
        
        self.storage.initial_load(self.start_time, self.pred_step, self.demo_mode)
        

        ### LOOP:
        while not self.stop_event.is_set() and (self.loop < max_loop or no_loop_limit):

            print(f"\ncommencing loop no. {self.loop}..\n")

            elapsed = self.loop_content()

            print(f"\n.. finished loop no. {self.loop}: took {(elapsed):.2f} seconds\n\n")

            self.loop += 1

            # if attained loop limit, break before sleep

            if (not no_loop_limit and self.loop >= max_loop):
                print("Loop stopped before sleeping\n")
                self.stop()
                break

            # else: sleep for rest of time in prediction interval

            wait_in_seconds = pred_interval * 60
            sleep_time = wait_in_seconds - elapsed

            print(f"- Sleeping for {sleep_time:.2f} seconds..")

            self.sleep(sleep_time)

            print(f"- Done Sleeping ! \n")

            
        
        print("\nSimulation ended\n\n------------------\n")

        # update gui one final time

        self.stop()

        plot_pv(self.storage.get_full_entries(), self.sliding_window, self.pred_interval)

        plot_rmse(self.storage.get_full_entries(), self.sliding_window, self.pred_interval)

        self.storage.save_storage()

        # save plot and storage

    
    ## what happens every loop
    def loop_content(self):

        ti = time()

        timestamp = datetime.now()
        timestamp = timestamp.replace(microsecond=0)

        ts = timestamp # store for testing

        if self.demo_mode:

            timestamp = self.demo_start_time
            timestamp = advance_time(timestamp, self.loop, self.pred_interval) # warning ! not pred interval but pred horizon !

            if timestamp >= self.demo_end_time:

                # if we arrive at the end of the closed interval of time, we set the stop flag
                self.stop()
        


        timestamp, _ = self.storage.process_new_input(timestamp)

        print(f"\n---------------------head start loop: {self.storage.head}\nahead start loop:{self.storage.ahead}\n")
        ##

        inputs_raw = self.storage.get_sequence( timestamp, self.sliding_window)

        output_dict = {
                "time_t":self.start_time, 
                "time_tplus":ts + timedelta(minutes=self.pred_interval), 
                "rmse": self.storage.get_by_cat("rmse"),
                "input_data":None,
                "output_data":None
            }

        output_dict["input_data"] = prepare_input( inputs_raw )

        if self.gui_update is not None:
            self.gui_update(output_dict)

        ##

        inputs_formatted = format_for_model(inputs_raw)

        inputs_normalized = normalize_list(inputs_formatted)

        x = inputs_normalized

        pred_normalized =  predict_from_sequence(self.model, x)

        pred = denormalize_pred(pred_normalized)

        print(f"\n---------------TIME: {timestamp}\n---------------INPUT: {inputs_raw}\n---------------OUTPUT: {pred}")

        pred_time = time() - ti

        self.storage.change_head(timestamp, self.pred_step, pred, pred_time)

        print(f"\n---------------------head end loop: {self.storage.head}\nahead end loop:{self.storage.ahead}\n")

        #output_strings = format_for_gui(inputs_formatted, self.storage.head, pred, pred_time, self.loop)

        ##
        
        output_dict["output_data"] = {
            "pred_power": pred,
            "pred_time": pred_time,
            "loop": self.loop,
            "time": timestamp
        }

        if self.gui_update is not None:
            self.gui_update(output_dict)

        return time() - ti







    def sleep(self, sleep_time):
        
        t0 = time()
        timeout = t0 + sleep_time


        print(f"progress: {' ' * 100}| ({0}%)", end="\r", flush=True)

        while not self.stop_event.is_set() and time() < timeout:

            progress_bar_advance(t0, sleep_time)

            continue

        if not self.stop_event.is_set():
            print(f"progress: {'#' * 100}| ({100}%)", end="\r", flush=True)


