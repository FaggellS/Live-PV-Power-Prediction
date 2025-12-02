"""load_weights.py
Load MATLAB .mat arrays and copy into a MatlabLSTM instance.


Assumptions based on your MATLAB outputs:
- LSTM layer has hidden_size=50
- MATLAB variables saved as:
- l2_inp_wb -> InputWeights (shape 200 x 6 == 4*H x input_size)
- l2_rec_wb -> RecurrentWeights (shape 200 x 50 == 4*H x H)
- l2_bias -> Bias (shape 200 x 1 == 4*H)
- l3_wb -> Fully connected weights (1 x 50)
- l3_bias -> Fully connected bias (scalar)


Strategy:
- Use scipy.io.loadmat to load arrays (works for v7 and non-v7.3 MAT-files saved as numeric arrays).
- Convert numpy arrays to torch tensors of dtype float32 and assign them into PyTorch LSTM/Linear parameters.
- For PyTorch LSTM, the gate order is the same we expect: (i, f, g, o) and MATLAB uses (i, f, c, o) which matches the mapping.
- For bias: MATLAB provides a single bias vector. PyTorch uses two bias tensors (bias_ih and bias_hh). We'll copy MATLAB bias into bias_ih and set bias_hh to zeros. This is the common pragmatic conversion that works for inference.


Note: if you find predictions differ slightly, try swapping a transpose in assignments — the loader prints shapes and will alert you if a transpose may be needed.
"""


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
    """Load .mat arrays and set PyTorch model weights in-place.


    Paths: files created from MATLAB (one array per file) or a single .mat containing keys.
    """

    # load with scipy (each file may contain a variable named 'ans' or the variable name itself)
    def load_first_array(path):
        d = sio.loadmat(path)
        # find first ndarray in the dict (skip meta keys)
        for k, v in d.items():
            if k.startswith("__"):
                continue
            if isinstance(v, np.ndarray):
                return v
        raise ValueError(f"No array found in {path}")


    W_in = load_first_array(l2_inp_wb_path) # expected shape (4*H, input_size)
    W_rec = load_first_array(l2_rec_wb_path) # expected shape (4*H, H)
    b_all = load_first_array(l2_bias_path) # expected shape (4*H, 1) or (4*H,)
    W_fc = load_first_array(l3_wb_path) # expected shape (1, H)
    b_fc = load_first_array(l3_bias_path) # scalar


    # reshape/clean
    W_in = np.squeeze(W_in)
    W_rec = np.squeeze(W_rec)
    b_all = np.squeeze(b_all)
    W_fc = np.squeeze(W_fc)
    b_fc = np.squeeze(b_fc)


    # print shapes for sanity
    print("Loaded shapes:")
    print("W_in", W_in.shape)
    print("W_rec", W_rec.shape)
    print("b_all", b_all.shape)
    print("W_fc", W_fc.shape)
    print("b_fc", getattr(b_fc, 'shape', ()) )


    H = model.hidden_size
    expected_Win_shape = (4 * H, model.input_size)
    expected_Wrec_shape = (4 * H, H)

    # Some MAT -> numpy orders can lead to transposed shapes; try to fix by transpose if mismatch
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


    # convert to tensors
    W_in_t = _to_tensor(W_in)
    W_rec_t = _to_tensor(W_rec)
    b_all_t = _to_tensor(b_all).reshape(-1)
    W_fc_t = _to_tensor(W_fc).reshape(1, H)
    b_fc_t = torch.tensor(float(b_fc), dtype=torch.float32)

    # assign into model.lstm weights
    # PyTorch names: weight_ih_l0 (4H x input_size), weight_hh_l0 (4H x H), bias_ih_l0 (4H), bias_hh_l0 (4H)
    with torch.no_grad():
        model.lstm.weight_ih_l0.copy_(W_in_t)
        model.lstm.weight_hh_l0.copy_(W_rec_t)


        # Copy matlab single bias into bias_ih, set bias_hh to zeros (common pragmatic choice)
        model.lstm.bias_ih_l0.copy_(b_all_t)
        model.lstm.bias_hh_l0.zero_()


        # Fully connected
        model.fc.weight.copy_(W_fc_t)
        model.fc.bias.copy_(b_fc_t.view(-1))


    print("Weights loaded into PyTorch model")
    return model

if __name__ == "__main__":
    # small usage example; adjust paths to where you put your uploaded .mat files
    model = MatlabLSTM()
    model = load_matlab_weights(
        model,
        l2_inp_wb_path="model/weights/l2_inp_wb.mat",
        l2_rec_wb_path="model/weights/l2_rec_wb.mat",
        l2_bias_path="model/weights/l2_bias.mat",
        l3_wb_path="model/weights/l3_wb.mat",
        l3_bias_path="model/weights/l3_bias.mat",
    )

    # quick forward pass smoke test
    import torch
    x = torch.zeros(2, 1, 6) # seq_len=2, batch=1, input=6
    y = model(x)
    print("y:", y)