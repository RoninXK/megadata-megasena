from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_DADOS = (
    PASTA_PROJETO
    / "data"
    / "processed"
    / "mega_sena_tratada.csv"
)

PASTA_SAIDA = (
    PASTA_PROJETO
    / "data"
    / "processed"
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
print("MEGADATA - ANÁLISE ESTATÍSTICA")
print("========================================\n")


# ============================================================
# 1. CARREGAR DADOS
# ============================================================

df = pd.read_csv(
    ARQUIVO_DADOS
)

print(f"Concursos carregados: {len(df)}")


# ============================================================
# 2. JUNTAR TODAS AS DEZENAS
# ============================================================

todas_dezenas = (
    df[COLUNAS_DEZENAS]
    .stack()
    .astype(int)
)

print(
    f"Total de dezenas analisadas: "
    f"{len(todas_dezenas)}"
)


# ============================================================
# 3. FREQUÊNCIA DE CADA DEZENA
# ============================================================

frequencia = (
    todas_dezenas
    .value_counts()
    .reindex(
        range(1, 61),
        fill_value=0
    )
)

frequencia = frequencia.sort_index()


frequencia_df = pd.DataFrame({
    "Dezena": frequencia.index,
    "Quantidade": frequencia.values
})

frequencia_df["Percentual"] = (
    frequencia_df["Quantidade"]
    / len(df)
    * 100
)


print("\n========================================")
print("FREQUÊNCIA DAS DEZENAS")
print("========================================\n")

for _, linha in frequencia_df.iterrows():

    print(
        f"{int(linha['Dezena']):02d} -> "
        f"{int(linha['Quantidade'])} vezes "
        f"({linha['Percentual']:.2f}%)"
    )


# ============================================================
# 4. TOP 10 MAIS SORTEADAS
# ============================================================

mais_sorteadas = (
    frequencia_df
    .sort_values(
        by="Quantidade",
        ascending=False
    )
    .head(10)
)


print("\n========================================")
print("TOP 10 MAIS SORTEADAS")
print("========================================\n")

for posicao, (_, linha) in enumerate(
    mais_sorteadas.iterrows(),
    start=1
):

    print(
        f"{posicao:02d}. "
        f"Dezena {int(linha['Dezena']):02d} -> "
        f"{int(linha['Quantidade'])} vezes"
    )


# ============================================================
# 5. TOP 10 MENOS SORTEADAS
# ============================================================

menos_sorteadas = (
    frequencia_df
    .sort_values(
        by="Quantidade",
        ascending=True
    )
    .head(10)
)


print("\n========================================")
print("TOP 10 MENOS SORTEADAS")
print("========================================\n")

for posicao, (_, linha) in enumerate(
    menos_sorteadas.iterrows(),
    start=1
):

    print(
        f"{posicao:02d}. "
        f"Dezena {int(linha['Dezena']):02d} -> "
        f"{int(linha['Quantidade'])} vezes"
    )


# ============================================================
# 6. PARES E ÍMPARES
# ============================================================

def contar_pares(linha):

    return sum(
        numero % 2 == 0
        for numero in linha[COLUNAS_DEZENAS]
    )


df["Qtd_Pares"] = df.apply(
    contar_pares,
    axis=1
)

df["Qtd_Impares"] = (
    6 - df["Qtd_Pares"]
)


paridade = (
    df.groupby(
        ["Qtd_Pares", "Qtd_Impares"]
    )
    .size()
    .reset_index(
        name="Quantidade"
    )
)

paridade["Percentual"] = (
    paridade["Quantidade"]
    / len(df)
    * 100
)

paridade = paridade.sort_values(
    by="Quantidade",
    ascending=False
)


print("\n========================================")
print("DISTRIBUIÇÃO PARES / ÍMPARES")
print("========================================\n")

for _, linha in paridade.iterrows():

    print(
        f"{int(linha['Qtd_Pares'])} pares / "
        f"{int(linha['Qtd_Impares'])} ímpares -> "
        f"{int(linha['Quantidade'])} concursos "
        f"({linha['Percentual']:.2f}%)"
    )


# ============================================================
# 7. SOMA DAS DEZENAS
# ============================================================

df["Soma"] = (
    df[COLUNAS_DEZENAS]
    .sum(axis=1)
)


print("\n========================================")
print("SOMA DAS DEZENAS")
print("========================================\n")

print(
    f"Média: {df['Soma'].mean():.2f}"
)

print(
    f"Mediana: {df['Soma'].median():.2f}"
)

print(
    f"Menor soma: {df['Soma'].min()}"
)

print(
    f"Maior soma: {df['Soma'].max()}"
)

print(
    f"Desvio padrão: {df['Soma'].std():.2f}"
)


# ============================================================
# 8. NÚMEROS BAIXOS E ALTOS
# ============================================================

def contar_baixos(linha):

    return sum(
        numero <= 30
        for numero in linha[COLUNAS_DEZENAS]
    )


df["Qtd_Baixos"] = df.apply(
    contar_baixos,
    axis=1
)

df["Qtd_Altos"] = (
    6 - df["Qtd_Baixos"]
)


baixos_altos = (
    df.groupby(
        ["Qtd_Baixos", "Qtd_Altos"]
    )
    .size()
    .reset_index(
        name="Quantidade"
    )
)

baixos_altos["Percentual"] = (
    baixos_altos["Quantidade"]
    / len(df)
    * 100
)

baixos_altos = baixos_altos.sort_values(
    by="Quantidade",
    ascending=False
)


print("\n========================================")
print("NÚMEROS BAIXOS / ALTOS")
print("========================================\n")

for _, linha in baixos_altos.iterrows():

    print(
        f"{int(linha['Qtd_Baixos'])} baixos / "
        f"{int(linha['Qtd_Altos'])} altos -> "
        f"{int(linha['Quantidade'])} concursos "
        f"({linha['Percentual']:.2f}%)"
    )


# ============================================================
# 9. DISTRIBUIÇÃO POR FAIXAS
# ============================================================

faixas = {
    "01-10": (1, 10),
    "11-20": (11, 20),
    "21-30": (21, 30),
    "31-40": (31, 40),
    "41-50": (41, 50),
    "51-60": (51, 60),
}

resultado_faixas = []


print("\n========================================")
print("DISTRIBUIÇÃO POR FAIXAS")
print("========================================\n")


for nome, (inicio, fim) in faixas.items():

    quantidade = (
        (
            (todas_dezenas >= inicio)
            &
            (todas_dezenas <= fim)
        )
        .sum()
    )

    percentual = (
        quantidade
        / len(todas_dezenas)
        * 100
    )

    resultado_faixas.append({
        "Faixa": nome,
        "Quantidade": quantidade,
        "Percentual": percentual
    })

    print(
        f"{nome} -> "
        f"{quantidade} dezenas "
        f"({percentual:.2f}%)"
    )


faixas_df = pd.DataFrame(
    resultado_faixas
)


# ============================================================
# 10. ATRASO ATUAL DAS DEZENAS
# ============================================================

ultimo_concurso = (
    df["Concurso"]
    .max()
)

atrasos = []


for numero in range(1, 61):

    concursos_com_numero = df[
        df[COLUNAS_DEZENAS]
        .eq(numero)
        .any(axis=1)
    ]

    ultimo_aparecimento = (
        concursos_com_numero["Concurso"]
        .max()
    )

    atraso = (
        ultimo_concurso
        - ultimo_aparecimento
    )

    atrasos.append({
        "Dezena": numero,
        "Ultimo_Concurso": ultimo_aparecimento,
        "Atraso": atraso
    })


atrasos_df = pd.DataFrame(
    atrasos
)

atrasos_df = atrasos_df.sort_values(
    by="Atraso",
    ascending=False
)


print("\n========================================")
print("TOP 10 DEZENAS MAIS ATRASADAS")
print("========================================\n")


for posicao, (_, linha) in enumerate(
    atrasos_df.head(10).iterrows(),
    start=1
):

    print(
        f"{posicao:02d}. "
        f"Dezena {int(linha['Dezena']):02d} -> "
        f"{int(linha['Atraso'])} concursos sem aparecer"
    )


# ============================================================
# 11. SALVAR RESULTADOS
# ============================================================

frequencia_df.to_csv(
    PASTA_SAIDA / "frequencia_dezenas.csv",
    index=False,
    encoding="utf-8-sig"
)

paridade.to_csv(
    PASTA_SAIDA / "distribuicao_paridade.csv",
    index=False,
    encoding="utf-8-sig"
)

baixos_altos.to_csv(
    PASTA_SAIDA / "distribuicao_baixos_altos.csv",
    index=False,
    encoding="utf-8-sig"
)

faixas_df.to_csv(
    PASTA_SAIDA / "distribuicao_faixas.csv",
    index=False,
    encoding="utf-8-sig"
)

atrasos_df.to_csv(
    PASTA_SAIDA / "atraso_dezenas.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\n========================================")
print("ANÁLISE CONCLUÍDA COM SUCESSO")
print("========================================\n")

print("Arquivos gerados:")

print(" - frequencia_dezenas.csv")
print(" - distribuicao_paridade.csv")
print(" - distribuicao_baixos_altos.csv")
print(" - distribuicao_faixas.csv")
print(" - atraso_dezenas.csv")