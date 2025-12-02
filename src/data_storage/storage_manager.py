from data_processing.input_manager import InputManager
from data_processing.validation_metrics import RMSE
import pandas as pd
from datetime import datetime

from os.path import dirname, join as pjoin

class Storage:

    

    def __init__(self):

        self.path_to_output= pjoin("..", "output", "output_data.csv")
        
        self.input_manager = InputManager()

        self.rmse = RMSE()

        self.df = None

        self.head = {"irradiance":-1, "temperature":-1, "true_power":-1, "pred_power":-1, "pred_time":-1, "rmse":-1, "state":"empty"}
        self.ahead = []

###

    def initial_load(self, timestamp, pred_step, is_demo_mode):

        self.input_manager.set_demo_mode(is_demo_mode)
        df = self.input_manager.load_current(timestamp)

        if df is not None:
            self.df = df


        for i in range(pred_step):


            self.ahead.append( {"irradiance":-1, "temperature":-1, "true_power":-1, "pred_power":-1, "pred_time":-1, "rmse":-1, "state":"empty"} )


###

    def process_new_input(self, timestamp):

        #timestamp, current_df = self.input_manager.load_current(timestamp)

        #current_entry = pd.DataFrame([ current_df.iloc[-1] ])

        ts, current_entry = self.input_manager.get_last_entry(timestamp)

        self.update_head(current_entry["irradiance"].item(), current_entry["temperature"].item(), current_entry["true_power"].item())

        return ts, self.head
    

###

    def update_head(self, irr, temp, true_pv):

        self.head["irradiance"] = irr
        self.head["temperature"] = temp
        self.head["true_power"] = true_pv

        if self.head["state"] == "empty":

            self.head["state"] = "raw"

        elif self.head["state"] == "prediction":

            self.head["rmse"] = self.rmse.compute_new(self.head["true_power"], self.head["pred_power"])
            self.head["state"] = "full"



###

    def get_sequence(self, timestamp, sliding_window):

        head_df = pd.DataFrame(self.head, index = [timestamp])

        return pd.concat([self.get_k_latest(sliding_window - 1), head_df], axis=0)



    def get_k_latest(self, k):

        return self.df.iloc[-k:,:]
    

    def get_by_cat(self, category):

        full_entries = self.get_full_entries()

        return [*full_entries[category]]
    

    def get_full_entries(self):

        return self.df[ self.df["state"] == "full" ]
    
    
    def save_storage(self):

        full_entries = self.get_full_entries()

        full_entries.to_csv(self.path_to_output, index=True)
 ###   
    
    def change_head(self, timestamp, pred_step, pred_value, pred_speed):

        ## update the corresponding entry ahead with the pred and computation speed
        self.ahead[pred_step - 1] = {"irradiance":-1, "temperature":-1, "true_power":-1, "pred_power":pred_value, "pred_time":pred_speed, "rmse":-1, "state":"prediction"}

        ## store current head into df
        self.store_head(timestamp)

        ## pop the ahead list and update the head
        self.head = self.ahead.pop(0)

        self.ahead.append( {"irradiance":-1, "temperature":-1, "true_power":-1, "pred_power":-1, "pred_time":-1, "rmse":-1, "state":"empty"} )

    

###

    def store_head(self, timestamp):

        head_df = pd.DataFrame(self.head, index = [timestamp])

        self.df = pd.concat([self.df, head_df], axis=0)
