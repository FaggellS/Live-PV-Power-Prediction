

import numpy as np
import torch
import scipy.io as sio
from model.model import MatlabLSTM


l2_inp_wb_path = "model/weights/l2_inp_wb.mat"
l2_rec_wb_path = "model/weights/l2_rec_wb.mat"
l2_bias_path = "model/weights/l2_bias.mat"
l3_wb_path = "model/weights/l3_wb.mat"
l3_bias_path = "model/weights/l3_bias.mat"

def _to_tensor(a):
    # ensure numpy float32 and contiguous
    a = np.array(a, dtype=np.float32)
    return torch.from_numpy(a)




def load_matlab_weights( model: MatlabLSTM ):
    """
    load .mat arrays and set PyTorch model weights in-place.
    """

   
    def load_first_array(path):
        d = sio.loadmat(path)
        
        for k, v in d.items():
            if k.startswith("__"):
                continue
            if isinstance(v, np.ndarray):
                return v
        raise ValueError(f"No array found in {path}")


    W_in = load_first_array(l2_inp_wb_path) # (4H, input_size)
    W_rec = load_first_array(l2_rec_wb_path) # (4H, H)
    b_all = load_first_array(l2_bias_path) #  (4H, 1) 
    W_fc = load_first_array(l3_wb_path) #  (1, H)
    b_fc = load_first_array(l3_bias_path) #


    # reshape/clean
    W_in = np.squeeze(W_in)
    W_rec = np.squeeze(W_rec)
    b_all = np.squeeze(b_all)
    W_fc = np.squeeze(W_fc)
    b_fc = np.squeeze(b_fc)

    H = model.hidden_size
    expected_Win_shape = (4 * H, model.input_size)
    expected_Wrec_shape = (4 * H, H)

    if W_in.shape != expected_Win_shape:
        if W_in.T.shape == expected_Win_shape:
            print("Transposing W_in to match expected shape")
            W_in = W_in.T
        else:
            raise RuntimeError(f"W_in shape {W_in.shape} does not match expected {expected_Win_shape}")


    if W_rec.shape != expected_Wrec_shape:
        if W_rec.T.shape == expected_Wrec_shape:
            print("Transposing W_rec to match expected shape")
            W_rec = W_rec.T
        else:
            raise RuntimeError(f"W_rec shape {W_rec.shape} does not match expected {expected_Wrec_shape}")


    W_in_t = _to_tensor(W_in)
    W_rec_t = _to_tensor(W_rec)
    b_all_t = _to_tensor(b_all).reshape(-1)
    W_fc_t = _to_tensor(W_fc).reshape(1, H)
    b_fc_t = torch.tensor(float(b_fc), dtype=torch.float32)

    with torch.no_grad():
        model.lstm.weight_ih_l0.copy_(W_in_t)
        model.lstm.weight_hh_l0.copy_(W_rec_t)


        model.lstm.bias_ih_l0.copy_(b_all_t)
        model.lstm.bias_hh_l0.zero_()


        model.fc.weight.copy_(W_fc_t)
        model.fc.bias.copy_(b_fc_t.view(-1))


    print("Weights loaded into PyTorch model")
    return model