"""
- input_size = 6
- hidden_size = 50
- num_layers = 1
"""


import torch
import torch.nn as nn


class MatlabLSTM(nn.Module):
    def __init__(self, input_size: int = 6, hidden_size: int = 50, num_layers: int = 1):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers


        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=False,
        )


        self.fc = nn.Linear(hidden_size, 1)


    def forward(self, x, hx=None):

        out, (h_n, c_n) = self.lstm(x, hx) 


        last = out[-1] 


        y = self.fc(last) 
        return y.squeeze(-1)


