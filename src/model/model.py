"""model.py
PyTorch LSTM that mirrors your MATLAB architecture:
- input_size = 6
- hidden_size = 50
- num_layers = 1
- output: single value via a fully-connected layer


The file only defines the class `MatlabLSTM`.
"""


import torch
import torch.nn as nn


class MatlabLSTM(nn.Module):
    def __init__(self, input_size: int = 6, hidden_size: int = 50, num_layers: int = 1):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers


        # single-layer LSTM
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=False, # we will use (seq_len, batch, feature) to match common RNN usage
        )


        # fully connected (last) layer
        self.fc = nn.Linear(hidden_size, 1)


    def forward(self, x, hx=None):
        """
        x: tensor shape (seq_len, batch, input_size)
        hx: tuple(h_0, c_0) each shape (num_layers, batch, hidden_size), optional
        returns: output tensor shape (batch, 1) -> last time-step prediction
        """
        # run LSTM
        out, (h_n, c_n) = self.lstm(x, hx) # out: (seq_len, batch, hidden_size)


        # we used MATLAB 'OutputMode', 'last' so take last time step
        last = out[-1] # (batch, hidden_size)


        # fully connected to single value
        y = self.fc(last) # (batch, 1)
        return y.squeeze(-1) # (batch,)




if __name__ == "__main__":
    # quick smoke test
    m = MatlabLSTM()
    x = torch.randn(2, 1, 6) # seq_len=2, batch=1
    y = m(x)
    print(y.shape) # (1,)