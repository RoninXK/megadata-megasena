from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent

PASTA_DADOS = (
    PASTA_PROJETO
    / "data"
    / "processed"
)

PASTA_IMAGENS = (
    PASTA_PROJETO
    / "images"
)

PASTA_IMAGENS.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# CARREGAR DADOS
# ============================================================

frequencia = pd.read_csv(
    PASTA_DADOS / "frequencia_dezenas.csv"
)

atrasos = pd.read_csv(
    PASTA_DADOS / "atraso_dezenas.csv"
)

paridade = pd.read_csv(
    PASTA_DADOS / "distribuicao_paridade.csv"
)

faixas = pd.read_csv(
    PASTA_DADOS / "distribuicao_faixas.csv"
)

dados = pd.read_csv(
    PASTA_DADOS / "mega_sena_tratada.csv"
)

COLUNAS_DEZENAS = [
    "bola 1",
    "bola 2",
    "bola 3",
    "bola 4",
    "bola 5",
    "bola 6",
]


print("\n========================================")
print("MEGADATA - GERAÇÃO DE GRÁFICOS")
print("========================================\n")


# ============================================================
# 1. FREQUÊNCIA DAS 60 DEZENAS
# ============================================================

plt.figure(figsize=(14, 6))

plt.bar(
    frequencia["Dezena"],
    frequencia["Quantidade"]
)

plt.title(
    "Frequência das dezenas da Mega-Sena"
)

plt.xlabel(
    "Dezena"
)

plt.ylabel(
    "Quantidade de aparições"
)

plt.xticks(
    range(1, 61, 2)
)

plt.tight_layout()

arquivo = (
    PASTA_IMAGENS
    / "frequencia_60_dezenas.png"
)

plt.savefig(
    arquivo,
    dpi=300
)

plt.close()

print(
    "Gráfico criado: frequencia_60_dezenas.png"
)


# ============================================================
# 2. TOP 10 MAIS SORTEADAS
# ============================================================

top10 = (
    frequencia
    .sort_values(
        by="Quantidade",
        ascending=False
    )
    .head(10)
    .sort_values(
        by="Quantidade",
        ascending=True
    )
)


plt.figure(figsize=(10, 6))

plt.barh(
    top10["Dezena"].astype(str),
    top10["Quantidade"]
)

plt.title(
    "Top 10 dezenas mais sorteadas"
)

plt.xlabel(
    "Quantidade de aparições"
)

plt.ylabel(
    "Dezena"
)

plt.tight_layout()

arquivo = (
    PASTA_IMAGENS
    / "top10_mais_sorteadas.png"
)

plt.savefig(
    arquivo,
    dpi=300
)

plt.close()

print(
    "Gráfico criado: top10_mais_sorteadas.png"
)


# ============================================================
# 3. TOP 10 MAIS ATRASADAS
# ============================================================

top10_atrasadas = (
    atrasos
    .sort_values(
        by="Atraso",
        ascending=False
    )
    .head(10)
    .sort_values(
        by="Atraso",
        ascending=True
    )
)


plt.figure(figsize=(10, 6))

plt.barh(
    top10_atrasadas["Dezena"].astype(str),
    top10_atrasadas["Atraso"]
)

plt.title(
    "Top 10 dezenas mais atrasadas"
)

plt.xlabel(
    "Concursos sem aparecer"
)

plt.ylabel(
    "Dezena"
)

plt.tight_layout()

arquivo = (
    PASTA_IMAGENS
    / "top10_atrasadas.png"
)

plt.savefig(
    arquivo,
    dpi=300
)

plt.close()

print(
    "Gráfico criado: top10_atrasadas.png"
)


# ============================================================
# 4. DISTRIBUIÇÃO PARES / ÍMPARES
# ============================================================

paridade["Combinacao"] = (
    paridade["Qtd_Pares"].astype(str)
    + "P / "
    + paridade["Qtd_Impares"].astype(str)
    + "I"
)


plt.figure(figsize=(9, 6))

plt.bar(
    paridade["Combinacao"],
    paridade["Quantidade"]
)

plt.title(
    "Distribuição de números pares e ímpares"
)

plt.xlabel(
    "Combinação"
)

plt.ylabel(
    "Quantidade de concursos"
)

plt.tight_layout()

arquivo = (
    PASTA_IMAGENS
    / "distribuicao_paridade.png"
)

plt.savefig(
    arquivo,
    dpi=300
)

plt.close()

print(
    "Gráfico criado: distribuicao_paridade.png"
)


# ============================================================
# 5. DISTRIBUIÇÃO POR FAIXAS
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    faixas["Faixa"],
    faixas["Quantidade"]
)

plt.title(
    "Distribuição das dezenas por faixa"
)

plt.xlabel(
    "Faixa"
)

plt.ylabel(
    "Quantidade de aparições"
)

plt.tight_layout()

arquivo = (
    PASTA_IMAGENS
    / "distribuicao_faixas.png"
)

plt.savefig(
    arquivo,
    dpi=300
)

plt.close()

print(
    "Gráfico criado: distribuicao_faixas.png"
)


# ============================================================
# 6. HISTOGRAMA DA SOMA DAS DEZENAS
# ============================================================

dados["Soma"] = (
    dados[COLUNAS_DEZENAS]
    .sum(axis=1)
)


plt.figure(figsize=(10, 6))

plt.hist(
    dados["Soma"],
    bins=30
)

plt.title(
    "Distribuição da soma das dezenas"
)

plt.xlabel(
    "Soma das 6 dezenas"
)

plt.ylabel(
    "Quantidade de concursos"
)

plt.tight_layout()

arquivo = (
    PASTA_IMAGENS
    / "distribuicao_somas.png"
)

plt.savefig(
    arquivo,
    dpi=300
)

plt.close()

print(
    "Gráfico criado: distribuicao_somas.png"
)


# ============================================================
# FINAL
# ============================================================

print("\n========================================")
print("GRÁFICOS GERADOS COM SUCESSO")
print("========================================")

print(
    f"\nArquivos salvos em:\n{PASTA_IMAGENS}"
)