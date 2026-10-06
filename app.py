from pathlib import Path
import random

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="MegaData",
    page_icon="🎰",
    layout="wide",
)


# ============================================================
# CAMINHOS
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent

PASTA_DADOS = (
    PASTA_PROJETO
    / "data"
    / "processed"
)

ARQUIVO_PRINCIPAL = (
    PASTA_DADOS
    / "mega_sena_tratada.csv"
)

ARQUIVO_FREQUENCIA = (
    PASTA_DADOS
    / "frequencia_dezenas.csv"
)

ARQUIVO_ATRASOS = (
    PASTA_DADOS
    / "atraso_dezenas.csv"
)

ARQUIVO_PARIDADE = (
    PASTA_DADOS
    / "distribuicao_paridade.csv"
)

ARQUIVO_FAIXAS = (
    PASTA_DADOS
    / "distribuicao_faixas.csv"
)

ARQUIVO_BACKTEST = (
    PASTA_DADOS
    / "backtest_resumo.csv"
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
# CARREGAMENTO DOS DADOS
# ============================================================

@st.cache_data
def carregar_dados():

    dados = pd.read_csv(
        ARQUIVO_PRINCIPAL
    )

    dados["Data"] = pd.to_datetime(
        dados["Data"],
        dayfirst=True,
        errors="coerce"
    )

    frequencia = pd.read_csv(
        ARQUIVO_FREQUENCIA
    )

    atrasos = pd.read_csv(
        ARQUIVO_ATRASOS
    )

    paridade = pd.read_csv(
        ARQUIVO_PARIDADE
    )

    faixas = pd.read_csv(
        ARQUIVO_FAIXAS
    )

    # Garantir tipos corretos
    frequencia["Dezena"] = (
        frequencia["Dezena"]
        .astype(int)
    )

    atrasos["Dezena"] = (
        atrasos["Dezena"]
        .astype(int)
    )

    # Muito importante:
    # impede o Plotly de interpretar 01-10 como data
    faixas["Faixa"] = (
        faixas["Faixa"]
        .astype(str)
    )

    return (
        dados,
        frequencia,
        atrasos,
        paridade,
        faixas,
    )


try:

    (
        dados,
        frequencia,
        atrasos,
        paridade,
        faixas,
    ) = carregar_dados()

except FileNotFoundError as erro:

    st.error(
        "Um ou mais arquivos necessários não foram encontrados."
    )

    st.code(str(erro))

    st.info(
        "Execute primeiro tratamento.py e estatisticas.py."
    )

    st.stop()


# ============================================================
# FUNÇÕES DO GERADOR
# ============================================================

def gerar_aleatorio():

    return sorted(
        random.sample(
            range(1, 61),
            6
        )
    )


def gerar_por_frequencia():

    numeros = (
        frequencia["Dezena"]
        .astype(int)
        .tolist()
    )

    pesos = (
        frequencia["Quantidade"]
        .tolist()
    )

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

    if pares < 2 or pares > 4:
        return False

    if baixos < 2 or baixos > 4:
        return False

    if soma < 100 or soma > 260:
        return False

    return True


def gerar_com_filtros():

    for _ in range(10000):

        jogo = gerar_por_frequencia()

        if jogo_valido(jogo):
            return jogo

    return gerar_aleatorio()


def mostrar_bolas(jogo):

    html = ""

    for numero in jogo:

        html += f"""
        <span style="
            display:inline-block;
            width:55px;
            height:55px;
            line-height:55px;
            text-align:center;
            margin:6px;
            border-radius:50%;
            background-color:#198754;
            color:white;
            font-size:20px;
            font-weight:bold;
        ">
        {numero:02d}
        </span>
        """

    return html


# ============================================================
# MENU
# ============================================================

st.sidebar.title("🎰 MegaData")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Visão Geral",
        "🔢 Dezenas",
        "📊 Estatísticas",
        "🎲 Gerador",
        "🧪 Backtest",
        "ℹ️ Sobre",
    ]
)


# ============================================================
# VISÃO GERAL
# ============================================================

if pagina == "🏠 Visão Geral":

    st.title(
        "🎰 MegaData"
    )

    st.subheader(
        "Análise Estatística da Mega-Sena"
    )

    st.write(
        """
        Projeto desenvolvido para análise de dados,
        estatística, visualização e experimentação
        com resultados históricos da Mega-Sena.
        """
    )

    ultimo_concurso = int(
        dados["Concurso"].max()
    )

    primeira_data = (
        dados["Data"].min()
    )

    ultima_data = (
        dados["Data"].max()
    )

    total_dezenas = (
        len(dados) * 6
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Concursos analisados",
        f"{len(dados):,}".replace(",", ".")
    )

    col2.metric(
        "Último concurso",
        ultimo_concurso
    )

    col3.metric(
        "Dezenas analisadas",
        f"{total_dezenas:,}".replace(",", ".")
    )

    col4.metric(
        "Período",
        f"{primeira_data.year} - {ultima_data.year}"
    )


    st.divider()


    # ========================================================
    # FREQUÊNCIA DAS 60 DEZENAS
    # ========================================================

    st.subheader(
        "Frequência das 60 dezenas"
    )

    fig = px.bar(
        frequencia,
        x="Dezena",
        y="Quantidade",
        labels={
            "Dezena": "Dezena",
            "Quantidade": "Quantidade de sorteios"
        }
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=5
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # MAIS SORTEADAS
    # ========================================================

    st.subheader(
        "Dezenas mais sorteadas"
    )

    top10 = (
        frequencia
        .sort_values(
            "Quantidade",
            ascending=False
        )
        .head(10)
        .copy()
    )

    top10["Dezena_fmt"] = (
        top10["Dezena"]
        .astype(int)
        .apply(
            lambda x: f"{x:02d}"
        )
    )

    fig = px.bar(
        top10,
        x="Dezena_fmt",
        y="Quantidade",
        text="Quantidade",
        labels={
            "Dezena_fmt": "Dezena",
            "Quantidade": "Quantidade"
        }
    )

    fig.update_xaxes(
        type="category"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DEZENAS
# ============================================================

elif pagina == "🔢 Dezenas":

    st.title(
        "🔢 Análise individual de dezenas"
    )

    numero = st.selectbox(
        "Escolha uma dezena",
        list(range(1, 61)),
        format_func=lambda x: f"{x:02d}"
    )


    # ========================================================
    # FREQUÊNCIA
    # ========================================================

    linha_frequencia = frequencia[
        frequencia["Dezena"] == numero
    ].iloc[0]

    quantidade = int(
        linha_frequencia["Quantidade"]
    )

    percentual = float(
        linha_frequencia["Percentual"]
    )


    # ========================================================
    # ATRASO
    # ========================================================

    linha_atraso = atrasos[
        atrasos["Dezena"] == numero
    ].iloc[0]

    ultimo = int(
        linha_atraso["Ultimo_Concurso"]
    )

    atraso = int(
        linha_atraso["Atraso"]
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Dezena",
        f"{numero:02d}"
    )

    col2.metric(
        "Aparições",
        quantidade
    )

    col3.metric(
        "% dos concursos",
        f"{percentual:.2f}%"
    )

    col4.metric(
        "Atraso atual",
        atraso
    )


    st.write(
        f"""
        A dezena **{numero:02d}** apareceu pela última vez
        no concurso **{ultimo}**.
        """
    )


    # ========================================================
    # HISTÓRICO
    # ========================================================

    concursos_numero = dados[
        dados[COLUNAS_DEZENAS]
        .eq(numero)
        .any(axis=1)
    ].copy()


    st.subheader(
        "Aparições ao longo do tempo"
    )

    concursos_numero["Apareceu"] = 1

    fig = px.scatter(
        concursos_numero,
        x="Data",
        y="Apareceu",
        hover_data=["Concurso"]
    )

    fig.update_yaxes(
        visible=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader(
        "Últimos concursos em que apareceu"
    )

    tabela = (
        concursos_numero[
            ["Concurso", "Data"]
        ]
        .sort_values(
            "Concurso",
            ascending=False
        )
        .head(15)
        .copy()
    )

    tabela["Data"] = (
        tabela["Data"]
        .dt.strftime("%d/%m/%Y")
    )

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ESTATÍSTICAS
# ============================================================

elif pagina == "📊 Estatísticas":

    st.title(
        "📊 Estatísticas"
    )


    # ========================================================
    # PARES / ÍMPARES
    # ========================================================

    st.subheader(
        "Distribuição de pares e ímpares"
    )

    paridade_grafico = (
        paridade.copy()
    )

    paridade_grafico["Combinação"] = (
        paridade_grafico["Qtd_Pares"]
        .astype(str)
        + " pares / "
        + paridade_grafico["Qtd_Impares"]
        .astype(str)
        + " ímpares"
    )

    fig = px.bar(
        paridade_grafico,
        x="Combinação",
        y="Quantidade",
        text="Quantidade",
        labels={
            "Combinação": "Distribuição",
            "Quantidade": "Quantidade de concursos"
        }
    )

    fig.update_xaxes(
        type="category"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # DISTRIBUIÇÃO POR FAIXAS
    # ========================================================

    st.subheader(
        "Distribuição por faixas"
    )

    faixas_grafico = (
        faixas.copy()
    )

    faixas_grafico["Faixa"] = (
        faixas_grafico["Faixa"]
        .astype(str)
    )

    ordem_faixas = [
        "01-10",
        "11-20",
        "21-30",
        "31-40",
        "41-50",
        "51-60",
    ]

    fig = px.bar(
        faixas_grafico,
        x="Faixa",
        y="Quantidade",
        text="Quantidade",
        labels={
            "Faixa": "Faixa de dezenas",
            "Quantidade": "Quantidade"
        },
        category_orders={
            "Faixa": ordem_faixas
        }
    )

    fig.update_xaxes(
        type="category",
        categoryorder="array",
        categoryarray=ordem_faixas
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # SOMAS
    # ========================================================

    st.subheader(
        "Distribuição da soma das dezenas"
    )

    dados_somas = (
        dados.copy()
    )

    dados_somas["Soma"] = (
        dados_somas[COLUNAS_DEZENAS]
        .sum(axis=1)
    )

    fig = px.histogram(
        dados_somas,
        x="Soma",
        nbins=30,
        labels={
            "Soma": "Soma das 6 dezenas"
        }
    )

    fig.update_layout(
        yaxis_title="Quantidade de concursos"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Média",
        f"{dados_somas['Soma'].mean():.2f}"
    )

    col2.metric(
        "Mediana",
        f"{dados_somas['Soma'].median():.2f}"
    )

    col3.metric(
        "Menor soma",
        int(
            dados_somas["Soma"].min()
        )
    )

    col4.metric(
        "Maior soma",
        int(
            dados_somas["Soma"].max()
        )
    )


    # ========================================================
    # DEZENAS MAIS ATRASADAS
    # ========================================================

    st.subheader(
        "Dezenas mais atrasadas"
    )

    top_atrasadas = (
        atrasos
        .sort_values(
            "Atraso",
            ascending=False
        )
        .head(10)
        .copy()
    )

    top_atrasadas["Dezena_fmt"] = (
        top_atrasadas["Dezena"]
        .astype(int)
        .apply(
            lambda x: f"{x:02d}"
        )
    )

    fig = px.bar(
        top_atrasadas,
        x="Dezena_fmt",
        y="Atraso",
        text="Atraso",
        labels={
            "Dezena_fmt": "Dezena",
            "Atraso": "Concursos sem aparecer"
        }
    )

    fig.update_xaxes(
        type="category"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# GERADOR
# ============================================================

elif pagina == "🎲 Gerador":

    st.title(
        "🎲 Gerador experimental de jogos"
    )

    st.warning(
        """
        Resultados históricos não aumentam a
        probabilidade matemática de prever
        sorteios futuros.

        Esta ferramenta possui finalidade
        exclusivamente educacional.
        """
    )


    metodo = st.selectbox(
        "Escolha o método",
        [
            "Aleatório",
            "Frequência histórica",
            "Estatístico com filtros",
        ]
    )


    quantidade_jogos = st.slider(
        "Quantidade de jogos",
        min_value=1,
        max_value=10,
        value=1
    )


    if st.button(
        "🎲 Gerar jogos",
        type="primary",
        use_container_width=True
    ):

        st.subheader(
            "Jogos gerados"
        )

        for numero_jogo in range(
            1,
            quantidade_jogos + 1
        ):

            if metodo == "Aleatório":

                jogo = gerar_aleatorio()

            elif metodo == "Frequência histórica":

                jogo = gerar_por_frequencia()

            else:

                jogo = gerar_com_filtros()


            st.markdown(
                f"### Jogo {numero_jogo}"
            )

            st.markdown(
                mostrar_bolas(jogo),
                unsafe_allow_html=True
            )

            pares = sum(
                numero % 2 == 0
                for numero in jogo
            )

            baixos = sum(
                numero <= 30
                for numero in jogo
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Soma",
                sum(jogo)
            )

            col2.metric(
                "Pares",
                pares
            )

            col3.metric(
                "Ímpares",
                6 - pares
            )

            col4.metric(
                "01-30",
                baixos
            )

            st.divider()


# ============================================================
# BACKTEST
# ============================================================

elif pagina == "🧪 Backtest":

    st.title(
        "🧪 Backtest dos métodos"
    )

    st.write(
        """
        O backtest compara os métodos utilizando
        somente informações disponíveis antes
        de cada concurso testado.
        """
    )


    if not ARQUIVO_BACKTEST.exists():

        st.warning(
            """
            O arquivo backtest_resumo.csv ainda
            não existe.

            Execute no terminal:

            python src/backtest.py
            """
        )

    else:

        backtest = pd.read_csv(
            ARQUIVO_BACKTEST
        )


        # ====================================================
        # MÉDIA DE ACERTOS
        # ====================================================

        st.subheader(
            "Comparação da média de acertos"
        )

        fig = px.bar(
            backtest,
            x="Metodo",
            y="Media_Acertos",
            text_auto=".3f",
            labels={
                "Metodo": "Método",
                "Media_Acertos": "Média de acertos"
            }
        )

        fig.update_xaxes(
            type="category"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ====================================================
        # TABELA
        # ====================================================

        st.subheader(
            "Resumo completo"
        )

        st.dataframe(
            backtest,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # DISTRIBUIÇÃO DOS ACERTOS
        # ====================================================

        colunas_acertos = [
            coluna
            for coluna in backtest.columns
            if coluna.startswith("Qtd_")
        ]


        if colunas_acertos:

            dados_grafico = (
                backtest.melt(
                    id_vars="Metodo",
                    value_vars=colunas_acertos,
                    var_name="Acertos",
                    value_name="Quantidade"
                )
            )

            dados_grafico["Acertos"] = (
                dados_grafico["Acertos"]
                .str.replace(
                    "Qtd_",
                    "",
                    regex=False
                )
                .str.replace(
                    "_Acertos",
                    "",
                    regex=False
                )
            )

            dados_grafico["Acertos"] = (
                dados_grafico["Acertos"]
                .astype(int)
            )


            st.subheader(
                "Distribuição dos acertos"
            )

            fig = px.bar(
                dados_grafico,
                x="Acertos",
                y="Quantidade",
                color="Metodo",
                barmode="group",
                labels={
                    "Metodo": "Método",
                    "Acertos": "Quantidade de acertos",
                    "Quantidade": "Número de jogos"
                }
            )

            fig.update_xaxes(
                dtick=1
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# SOBRE
# ============================================================

elif pagina == "ℹ️ Sobre":

    st.title(
        "ℹ️ Sobre o MegaData"
    )

    st.markdown(
        """
        ## MegaData

        Projeto educacional desenvolvido para
        demonstrar técnicas de:

        - Python
        - Pandas
        - análise de dados
        - estatística descritiva
        - visualização de dados
        - backtesting
        - Streamlit
        - Plotly
        - Git e GitHub

        ### Objetivo

        Analisar resultados históricos da
        Mega-Sena e comparar diferentes formas
        de geração experimental de combinações.

        ### Métodos disponíveis

        **Aleatório**

        Seleciona seis dezenas aleatoriamente.

        **Frequência histórica**

        Utiliza a frequência histórica das
        dezenas como peso na geração.

        **Estatístico com filtros**

        Utiliza frequência histórica e filtros
        de paridade, distribuição entre dezenas
        baixas e altas e soma total.

        ### Backtest

        O sistema também realiza testes
        retrospectivos para comparar os métodos
        com concursos históricos.

        Em cada teste, somente informações
        anteriores ao concurso analisado são
        utilizadas.

        Isso evita vazamento de dados futuros.

        ### Importante

        Sorteios lotéricos são eventos aleatórios.

        Frequências históricas, atrasos e outros
        padrões observados não garantem resultados
        futuros.

        Este projeto possui finalidade
        educacional e de demonstração de técnicas
        de análise de dados.
        """
    )