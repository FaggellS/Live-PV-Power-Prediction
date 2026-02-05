# Framework to Test Live PV Power Prediction

## Goal

> The objective for this project was to build a simulation framework in which we can operate a NN model that predicts PV power output in a near real-time setting.

For reference, here is how this project is structured:
![Project Architecture](/data/assets/architecture.jpg)

## Requirements

I have used the environment / package manager **uv** for this project, you are free to use it or not.

- Python version: >= 3.12
- uv version (optional): 0.1.0

## Environment and dependencies

#### Using uv

- You can install it quickly: [Link to the uv install page](https://docs.astral.sh/uv/getting-started/installation/)
- run `uv sync` from the project root to create the project environment and install dependencies.

#### Using pip (not tested)

If you'd rather avoid using uv, dependencies are listed in `requirements.txt`

- run `pip install -r requirements.txt` from the project root

## Adding the necessary files

In order for the program to work, you will need to add some files in the **`data`** folder found at the project root:

- Inside **`historical_data`**, the following files are required:
    - **`completed_dataset_irradiance.xlsx`** - cleaned dataset, with the timestamp as the 1st column and the corresponding value in the 2nd;
    - **`completed_dataset_temperature.xlsx`** - cleaned dataset, with the same structure as above;
    - **`reduced_dataset_mean_PVpower.xlsx`** - the clean dataset, with the same structure as above and the 10 minute intervals.

- Inside **`model_weigths`**, the following files are required:
    - **`l2_inp_wb.mat`** - the input weights for the second layer;
    - **`l2_rec_wb.mat`** - the recurrent weights for the second layer;
    - **`l2_bias.mat`** - the biases for the second layer;
    - **`l3_wb.mat`** - the weights for the final layer;
    - **`l3_bias.mat`** - the biases for the final layer.
 
If you want to modify the name of these files, the affected scripts are as follows:
- for **`historical-data`**, the only file that uses it is **`src/data_sources/hist_dataset.py`**.
- for **`model_weigths`**, the only file that uses it is **`src/model/load_weights.py`**.

#### Extracting your model's weights from Matlab

You will need to do the following to obtain the above-mentioned weights:
```
load lstm.mat
layers = net.Layers
```
For each layers containing weights (In our case we need `layers(2)` and `layers(3)` I think):
```
lX_inp_wb = specificLayer.InputWeights
lX_rec_wb = specificLayer.RecurrentWeights    % If this layer has them !
lX_bias = specificLayer.Bias
```
You can then download these as .mat objects and import them inside the `model_weights` folder.

For now, this project only supports the same architecture of LSTM, as was originally provided.

## Running the program
 
You can start the program by running **`main.py`** inside the **`src`** folder. When using uv, you can use the `uv run main.py` command inside src.

When you stop a simulation, useful information will be saved inside the folder **`output`**. You can also check the error and RMSE score in separate graphs (they are only generated after 6 loops). 

Those 3 files will be overwritten once you start a new simulation, and if you quit the program without explicitely stopping a simulation, the generated data will be lost.

## Notes

- The program cannot function with live input as of yet, as it still needs to integrate a stream of live PV input, and the stream of live meteo data only accounts for solar radiation, not irradiance directly.
- The demo mode fast forwards X minutes ahead after whichever interval you specified, taking historical data as if it were the current date and time. It runs during the span of two days and then terminates the simulation. You can modify the start and end time of the demo mode in **`src/simulation.py`**.






