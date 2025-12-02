"""predict.py
Small wrapper that shows the expected input format and how to call the model.


This assumes the sliding-window length is 2, and you supply `seq = [step_tminus1, step_t]` where each step is
an iterable of 6 numbers in the exact order used in MATLAB:
[irradiance_norm, temperature_norm, true_power_norm, hour_norm, day_norm, month_norm]


We build a tensor of shape (seq_len, batch=1, input_size) and call `model()`.


"""


import torch
from model.model import MatlabLSTM
from model.load_weights import load_matlab_weights


def predict_from_sequence(model, seq):
    """seq: list-like of two timesteps, each timestep list-like of length 6 (normalized already)
    returns denormalized scalar prediction (in original units)
    """
    device = next(model.parameters()).device


    arr = torch.tensor(seq, dtype=torch.float32, device=device)
    arr = arr.unsqueeze(1)


    model.eval()
    with torch.no_grad():
        out = model(arr) # shape (batch,)
    pred_norm = float(out.item())


    # denormalize predicted true_power (MATLAB used same mu/sigma for output)
    #pred = pred_norm * SIG_T + MU_T
    pred = pred_norm
    return pred



if __name__ == "__main__":
    # example usage
    model = MatlabLSTM()
    model = load_matlab_weights(
        model,
        l2_inp_wb_path="/mnt/data/l2_inp_wb.mat",
        l2_rec_wb_path="/mnt/data/l2_rec_wb.mat",
        l2_bias_path="/mnt/data/l2_bias.mat",
        l3_wb_path="/mnt/data/l3_wb.mat",
        l3_bias_path="/mnt/data/l3_bias.mat",
    )


    # Example from your XTestSeq{1} (already normalized values columns are: 6 x 2; we take columns as timesteps)
    # you gave this XTestSeq{1} as rows x cols; here we create corresponding two timesteps
    step_tminus1 = [-0.2388, 0.3228, -0.1384, 0.5652, 0.0, 0.7273]
    step_t = [-0.3304, 0.1705, -0.2393, 0.6087, 0.0, 0.7273]


    seq = [step_tminus1, step_t]
    pred = predict_from_sequence(model, seq)
    print("Predicted (denormalized):", pred)