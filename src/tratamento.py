from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_ENTRADA = (
    PASTA_PROJETO
    / "data"
    / "raw"
    / "mega_sena_asloterias_ate_concurso_3066_sorteio.xlsx"
)

ARQUIVO_SAIDA = (
    PASTA_PROJETO
    / "data"
    / "processed"
    / "mega_sena_tratada.csv"
)


COLUNAS_DEZENAS = [
    "bola 1",
    "bola 2",
    "bola 3",
    "bola 4",
    "bola 5",
    "bola 6",
]


# ============================================================
# INÍCIO
# ============================================================

print("\n========================================")
print("MEGADATA - TRATAMENTO DOS DADOS")
print("========================================\n")


# ============================================================
# 1. LEITURA DO EXCEL
# ============================================================

print("1. Lendo arquivo Excel...")

df = pd.read_excel(
    ARQUIVO_ENTRADA,
    sheet_name="mega_sena_www.asloterias.com.br",
    header=6
)

print("Arquivo carregado com sucesso!")
print(f"Concursos encontrados: {len(df)}")
print(f"Colunas encontradas: {len(df.columns)}")


# ============================================================
# 2. MOSTRAR COLUNAS
# ============================================================

print("\n2. Colunas encontradas:")

for coluna in df.columns:
    print(f" - {coluna}")


# ============================================================
# 3. VERIFICAR COLUNAS
# ============================================================

colunas_obrigatorias = [
    "Concurso",
    "Data",
    *COLUNAS_DEZENAS,
]

faltando = [
    coluna
    for coluna in colunas_obrigatorias
    if coluna not in df.columns
]

if faltando:
    print("\nERRO: faltam estas colunas:")
    print(faltando)
    raise SystemExit


print("\nEstrutura da planilha correta.")


# ============================================================
# 4. MANTER APENAS AS COLUNAS NECESSÁRIAS
# ============================================================

df = df[colunas_obrigatorias].copy()


# ============================================================
# 5. TRATAR CONCURSO
# ============================================================

df["Concurso"] = pd.to_numeric(
    df["Concurso"],
    errors="coerce"
)

df = df.dropna(subset=["Concurso"])

df["Concurso"] = df["Concurso"].astype(int)


# ============================================================
# 6. TRATAR DATAS
# ============================================================

df["Data"] = pd.to_datetime(
    df["Data"],
    format="%d/%m/%Y",
    errors="coerce"
)

datas_invalidas = df["Data"].isna().sum()

print("\n3. Verificando datas...")
print(f"Datas inválidas: {datas_invalidas}")


# ============================================================
# 7. TRATAR DEZENAS
# ============================================================

for coluna in COLUNAS_DEZENAS:

    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )


dezenas_invalidas = (
    df[COLUNAS_DEZENAS]
    .isna()
    .sum()
    .sum()
)

print("\n4. Verificando dezenas...")
print(f"Dezenas vazias ou inválidas: {dezenas_invalidas}")


# ============================================================
# 8. VERIFICAR INTERVALO 1-60
# ============================================================

fora_intervalo = (
    (df[COLUNAS_DEZENAS] < 1)
    |
    (df[COLUNAS_DEZENAS] > 60)
)

quantidade_fora = fora_intervalo.sum().sum()

print(
    f"Dezenas fora do intervalo 1-60: "
    f"{quantidade_fora}"
)


# ============================================================
# 9. VERIFICAR REPETIÇÃO DENTRO DO CONCURSO
# ============================================================

def possui_repeticao(linha):

    numeros = linha[COLUNAS_DEZENAS].tolist()

    return len(numeros) != len(set(numeros))


repeticoes = df.apply(
    possui_repeticao,
    axis=1
)

print(
    "Concursos com dezenas repetidas: "
    f"{repeticoes.sum()}"
)


# ============================================================
# 10. VERIFICAR CONCURSOS DUPLICADOS
# ============================================================

duplicados = df["Concurso"].duplicated().sum()

print("\n5. Verificando concursos...")
print(f"Concursos duplicados: {duplicados}")


# ============================================================
# 11. REMOVER DUPLICADOS
# ============================================================

df = df.drop_duplicates(
    subset="Concurso",
    keep="first"
)


# ============================================================
# 12. TRANSFORMAR DEZENAS EM INTEIROS
# ============================================================

for coluna in COLUNAS_DEZENAS:

    df[coluna] = df[coluna].astype(int)


# ============================================================
# 13. ORGANIZAR EM ORDEM CRESCENTE
# ============================================================

df = df.sort_values(
    by="Concurso",
    ascending=True
)

df = df.reset_index(drop=True)


# ============================================================
# 14. CRIAR PASTA DE SAÍDA
# ============================================================

ARQUIVO_SAIDA.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 15. SALVAR CSV TRATADO
# ============================================================

df.to_csv(
    ARQUIVO_SAIDA,
    index=False,
    encoding="utf-8-sig",
    date_format="%d/%m/%Y"
)


# ============================================================
# RESULTADO
# ============================================================

print("\n========================================")
print("TRATAMENTO CONCLUÍDO COM SUCESSO")
print("========================================")

print(f"\nTotal de concursos: {len(df)}")

print(
    f"Primeiro concurso: "
    f"{df['Concurso'].min()}"
)

print(
    f"Último concurso: "
    f"{df['Concurso'].max()}"
)

print(
    f"Primeira data: "
    f"{df['Data'].min().strftime('%d/%m/%Y')}"
)

print(
    f"Última data: "
    f"{df['Data'].max().strftime('%d/%m/%Y')}"
)

print("\nArquivo gerado:")

print(ARQUIVO_SAIDA)

print("\nPrimeiros concursos:")

print(df.head())

print("\nÚltimos concursos:")

print(df.tail())