import numpy as np

class RMSE:

    def __init__(self):
        self.l_pred = []
        self.l_true = []


        self.max_capacity = 22000 # 22.2 kW


    def compute_new(self, true, pred):

        self.l_true.append(true)
        self.l_pred.append(pred)

        return self.compute_RMSE()


    def compute_RMSE(self):

        norm = (np.array(self.l_true) - np.array(self.l_pred)) ** 2

        rmse = np.sqrt( np.mean (norm) ).item()

        relative_rmse = rmse / self.max_capacity

        return relative_rmse
