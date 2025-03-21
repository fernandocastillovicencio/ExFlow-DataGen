import numpy as np
from .extract_data import process_Ux_field
from .config import OUTPUT_NPY_PATH

def save_npy():
    """Salva o campo Ux como um arquivo .npy."""
    Ux_field = process_Ux_field()
    np.save(OUTPUT_NPY_PATH, Ux_field)
    print(f"Arquivo salvo: {OUTPUT_NPY_PATH}")

if __name__ == "__main__":
    save_npy()
