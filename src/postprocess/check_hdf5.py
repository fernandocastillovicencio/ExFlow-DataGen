import pandas as pd

# Caminho do arquivo HDF5 combinado
hdf5_file = "output/all_data.h5"

# Carregar os dados
df = pd.read_hdf(hdf5_file, key="dataset")

# Mostrar as primeiras linhas
print(df.head())

# Verificar número total de linhas
print(f"\n🔍 O arquivo contém {len(df)} linhas.")


# Caminho do arquivo CSV de saída
csv_file = "output/all_data.csv"

# Salvar como CSV
df.to_csv(csv_file, index=False)

print(f"\n✅ Arquivo CSV salvo em {csv_file}")
