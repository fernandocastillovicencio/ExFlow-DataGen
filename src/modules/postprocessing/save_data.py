import pickle
import numpy as np


def save_dataX(sdf1, flow_region, sdf2, output_file="dataX.pkl"):
    dataX = np.stack([sdf1, flow_region, sdf2], axis=0)
    dataX = np.expand_dims(dataX, axis=0)

    with open(output_file, "wb") as f:
        pickle.dump(dataX, f)

    print(f"✅ {output_file} salvo!")


def save_dataY(Ux_grid, Uy_grid, p_grid, output_file="dataY.pkl"):
    dataY = np.stack([Ux_grid, Uy_grid, p_grid], axis=0)
    dataY = np.expand_dims(dataY, axis=0)

    with open(output_file, "wb") as f:
        pickle.dump(dataY, f)

    print(f"✅ {output_file} salvo!")
