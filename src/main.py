from postprocess.save_npy import save_npy
from postprocess.plot_results import plot_Ux_field

def main():
    """Executa o pós-processamento do OpenFOAM."""
    save_npy()      # Processa os arquivos e salva o .npy
    plot_Ux_field() # Plota os dados salvos

if __name__ == "__main__":
    main()
