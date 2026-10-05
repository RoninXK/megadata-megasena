import pandas as pd

print("Iniciando leitura do Excel...")

arquivo = "data/raw/mega_sena_asloterias_ate_concurso_3066_sorteio.xlsx"

df = pd.read_excel(arquivo)

print("\nPrimeiras linhas:")
print(df.head())

print("\nColunas encontradas:")
print(df.columns.tolist())

print("\nQuantidade de linhas e colunas:")
print(df.shape)

print("\nLeitura concluída com sucesso!")