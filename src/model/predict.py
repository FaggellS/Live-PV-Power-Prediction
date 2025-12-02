import torch
from model.model import MatlabLSTM
from model.load_weights import load_matlab_weights


def predict_from_sequence(model, seq):
    device = next(model.parameters()).device


    arr = torch.tensor(seq, dtype=torch.float32, device=device)
    arr = arr.unsqueeze(1)


    model.eval()
    with torch.no_grad():
        out = model(arr)
    pred_norm = float(out.item())


    #pred = pred_norm * SIG_T + MU_T
    pred = pred_norm
    return pred

