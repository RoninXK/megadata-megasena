from pathlib import Path
import random
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

# Quantos concursos iniciais serão usados
# antes de começar a testar.
MINIMO_HISTORICO = 100

# Quantos jogos cada método irá gerar
# para cada concurso histórico.
JOGOS_POR_METODO = 5

# Garante resultados reproduzíveis.
random.seed(42)


# ============================================================
# CARREGAR DADOS
# ============================================================

print("\n========================================")
print("MEGADATA - BACKTEST HISTÓRICO")
print("========================================\n")

df = pd.read_csv(
    ARQUIVO_DADOS
)

df = df.sort_values(
    by="Concurso"
).reset_index(drop=True)

print(f"Concursos disponíveis: {len(df)}")
print(f"Histórico mínimo: {MINIMO_HISTORICO}")
print(f"Jogos por método: {JOGOS_POR_METODO}")


# ============================================================
# FUNÇÃO PARA CALCULAR FREQUÊNCIAS
# SOMENTE COM OS CONCURSOS DO PASSADO
# ============================================================

def calcular_frequencias(historico):

    todas_dezenas = (
        historico[COLUNAS_DEZENAS]
        .stack()
        .astype(int)
    )

    frequencia = (
        todas_dezenas
        .value_counts()
        .reindex(
            range(1, 61),
            fill_value=0
        )
    )

    # Soma 1 para evitar peso zero.
    frequencia = frequencia + 1

    return frequencia


# ============================================================
# MÉTODO 1 - ALEATÓRIO
# ============================================================

def gerar_aleatorio():

    jogo = random.sample(
        range(1, 61),
        6
    )

    return sorted(jogo)


# ============================================================
# MÉTODO 2 - FREQUÊNCIA HISTÓRICA
# ============================================================

def gerar_por_frequencia(frequencia):

    numeros = list(
        range(1, 61)
    )

    pesos = [
        frequencia[numero]
        for numero in numeros
    ]

    jogo = []

    while len(jogo) < 6:

        numero = random.choices(
            numeros,
            weights=pesos,
            k=1
        )[0]

        if numero not in jogo:
            jogo.append(numero)

    return sorted(jogo)


# ============================================================
# VALIDAÇÃO DO JOGO ESTATÍSTICO
# ============================================================

def jogo_valido(jogo):

    pares = sum(
        numero % 2 == 0
        for numero in jogo
    )

    baixos = sum(
        numero <= 30
        for numero in jogo
    )

    soma = sum(jogo)

    # Entre 2 e 4 pares
    if pares < 2 or pares > 4:
        return False

    # Entre 2 e 4 números de 1 a 30
    if baixos < 2 or baixos > 4:
        return False

    # Evita somas muito extremas
    if soma < 100 or soma > 260:
        return False

    return True


# ============================================================
# MÉTODO 3 - FREQUÊNCIA + FILTROS
# ============================================================

def gerar_com_filtros(frequencia):

    for _ in range(10000):

        jogo = gerar_por_frequencia(
            frequencia
        )

        if jogo_valido(jogo):
            return jogo

    return gerar_aleatorio()


# ============================================================
# CONTAR ACERTOS
# ============================================================

def contar_acertos(jogo, resultado):

    return len(
        set(jogo)
        &
        set(resultado)
    )


# ============================================================
# BACKTEST
# ============================================================

resultados_backtest = []

total_testes = (
    len(df)
    - MINIMO_HISTORICO
)

print(
    f"\nConcursos que serão testados: "
    f"{total_testes}"
)

print("\nIniciando backtest...\n")


for indice in range(
    MINIMO_HISTORICO,
    len(df)
):

    # Tudo que aconteceu ANTES
    # do concurso sendo testado.
    historico = df.iloc[:indice]

    concurso_alvo = df.iloc[indice]

    numero_concurso = int(
        concurso_alvo["Concurso"]
    )

    resultado_real = [
        int(concurso_alvo[coluna])
        for coluna in COLUNAS_DEZENAS
    ]

    # Frequência calculada apenas
    # com dados anteriores.
    frequencia = calcular_frequencias(
        historico
    )

    metodos = {
        "Aleatorio": gerar_aleatorio,
        "Frequencia": lambda:
            gerar_por_frequencia(
                frequencia
            ),
        "Estatistico_Filtros": lambda:
            gerar_com_filtros(
                frequencia
            ),
    }

    for nome_metodo, funcao in metodos.items():

        for numero_jogo in range(
            1,
            JOGOS_POR_METODO + 1
        ):

            jogo = funcao()

            acertos = contar_acertos(
                jogo,
                resultado_real
            )

            resultados_backtest.append({
                "Concurso": numero_concurso,
                "Metodo": nome_metodo,
                "Numero_Jogo": numero_jogo,
                "Jogo": "-".join(
                    f"{n:02d}"
                    for n in jogo
                ),
                "Resultado": "-".join(
                    f"{n:02d}"
                    for n in sorted(resultado_real)
                ),
                "Acertos": acertos,
            })

    # Mostrar progresso
    if (
        numero_concurso % 250 == 0
        or indice == len(df) - 1
    ):

        print(
            f"Processado até o concurso "
            f"{numero_concurso}"
        )


# ============================================================
# TRANSFORMAR EM DATAFRAME
# ============================================================

backtest_df = pd.DataFrame(
    resultados_backtest
)


# ============================================================
# RESUMO POR MÉTODO
# ============================================================

resumo = []

for metodo in backtest_df["Metodo"].unique():

    dados_metodo = backtest_df[
        backtest_df["Metodo"] == metodo
    ]

    media_acertos = (
        dados_metodo["Acertos"]
        .mean()
    )

    quantidade_testes = len(
        dados_metodo
    )

    linha = {
        "Metodo": metodo,
        "Testes": quantidade_testes,
        "Media_Acertos": media_acertos,
    }

    for acertos in range(0, 7):

        quantidade = (
            dados_metodo["Acertos"]
            == acertos
        ).sum()

        linha[
            f"Qtd_{acertos}_Acertos"
        ] = quantidade

    resumo.append(linha)


resumo_df = pd.DataFrame(
    resumo
)


# ============================================================
# EXIBIR RESULTADOS
# ============================================================

print("\n========================================")
print("RESULTADO DO BACKTEST")
print("========================================\n")

for _, linha in resumo_df.iterrows():

    print(
        f"MÉTODO: {linha['Metodo']}"
    )

    print(
        f"Testes realizados: "
        f"{int(linha['Testes'])}"
    )

    print(
        f"Média de acertos: "
        f"{linha['Media_Acertos']:.4f}"
    )

    print(
        f"0 acertos: "
        f"{int(linha['Qtd_0_Acertos'])}"
    )

    print(
        f"1 acerto: "
        f"{int(linha['Qtd_1_Acertos'])}"
    )

    print(
        f"2 acertos: "
        f"{int(linha['Qtd_2_Acertos'])}"
    )

    print(
        f"3 acertos: "
        f"{int(linha['Qtd_3_Acertos'])}"
    )

    print(
        f"4 acertos: "
        f"{int(linha['Qtd_4_Acertos'])}"
    )

    print(
        f"5 acertos: "
        f"{int(linha['Qtd_5_Acertos'])}"
    )

    print(
        f"6 acertos: "
        f"{int(linha['Qtd_6_Acertos'])}"
    )

    print("----------------------------------------")


# ============================================================
# MELHORES RESULTADOS
# ============================================================

print("\n========================================")
print("MELHORES RESULTADOS ENCONTRADOS")
print("========================================\n")


melhores = (
    backtest_df
    .sort_values(
        by="Acertos",
        ascending=False
    )
    .head(15)
)

print(
    melhores[
        [
            "Concurso",
            "Metodo",
            "Jogo",
            "Resultado",
            "Acertos",
        ]
    ].to_string(
        index=False
    )
)


# ============================================================
# SALVAR ARQUIVOS
# ============================================================

ARQUIVO_BACKTEST = (
    PASTA_SAIDA
    / "backtest_resultados.csv"
)

ARQUIVO_RESUMO = (
    PASTA_SAIDA
    / "backtest_resumo.csv"
)


backtest_df.to_csv(
    ARQUIVO_BACKTEST,
    index=False,
    encoding="utf-8-sig"
)

resumo_df.to_csv(
    ARQUIVO_RESUMO,
    index=False,
    encoding="utf-8-sig"
)


print("\n========================================")
print("BACKTEST CONCLUÍDO")
print("========================================")

print("\nArquivos gerados:")

print(
    " - backtest_resultados.csv"
)

print(
    " - backtest_resumo.csv"
)