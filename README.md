# Framework to Test Live PV Power Prediction

I have used the environment / package manager **uv** for this project, you are free to use it or not.

## Requirements

- Python version: >= 3.12
- uv version (optional): 0.1.0

## Environment and dependencies

### Using uv

- You can install it quickly: https://docs.astral.sh/uv/getting-started/installation/
- run 'uv sync' from the project root to create the project environment and install dependencies.

### Using pip (not tested)

If you'd rather avoid using uv, dependencies are listed in 'requirements.txt'

- run 'pip install -r requirements.txt' from the project root

## Adding the necessary files

**Before all else**: in order for the program to work, you will need to add some files in the **'data'** folder found at the project root:

- Inside **'historical-data'**, the following files are required:
    - **'completed_dataset_irradiance.xlsx'** - cleaned dataset, with the timestamp as the first column and the corresponding irradiance in the second;
    - **'completed_dataset_temperature.xlsx'** - cleaned dataset, with the same structure as above;
    - **'reduced_dataset_mean_PVpower.xlsx'** - the clean dataset, with the same structure as above and the 10 minute intervals.

- Inside **'model_weigths'**, the following files are required:
    - **'l2_inp_wb.mat'** - the input weights for the second layer;
    - **'l2_rec_wb.mat'** - the recurrent weights for the second layer;
    - **'l2_bias.mat'** - the biases for the second layer;
    - **'l3_wb.mat'** - the weights for the final layer;
    - **'l3_bias.mat'** - the biases for the final layer;

### Extracting your model's weights from Matlab

You will need to do the following to obtain the above-mentioned weights:
```
load lstm.mat
layers = net.Layers
```
For each layers containing weights (In our case we need `layers(2)` and `layers(3)` I think):
```
lX_inp_wb = specificLayer.InputWeights
lX_rec_wb = specificLayer.RecurrentWeights # If this layer has them !
lX_bias = specificLayer.Bias
```
You can then download these as .mat objects and import them inside the 'model_weights' folder.

For now, this project only supports the same architecture of LSTM, as was originally provided.

## Running the program
 
You can start the program by running **'main.py'** inside the **`src`** folder. When using uv, you can use the `uv run main.py` command inside src.

When you stop a simulation, useful information will be saved inside the folder **'output'**. You can also check the error and RMSE score in separate graphs. 

Those 3 files will be overwritten once you start a new simulation, and if you quit the program without explicitely stopping a simulation, the generated data will be lost.

