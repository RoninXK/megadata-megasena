from pathlib import Path
import random
import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_FREQUENCIA = (
    PASTA_PROJETO
    / "data"
    / "processed"
    / "frequencia_dezenas.csv"
)


# ============================================================
# CARREGAR DADOS
# ============================================================

frequencia = pd.read_csv(
    ARQUIVO_FREQUENCIA
)


# ============================================================
# GERADOR ALEATÓRIO
# ============================================================

def gerar_aleatorio():

    jogo = random.sample(
        range(1, 61),
        6
    )

    return sorted(jogo)


# ============================================================
# GERADOR BASEADO EM FREQUÊNCIA
# ============================================================

def gerar_por_frequencia():

    numeros = frequencia["Dezena"].tolist()

    pesos = frequencia["Quantidade"].tolist()

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
# VALIDAÇÃO DO JOGO
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

    # Queremos entre 2 e 4 números pares
    if pares < 2 or pares > 4:
        return False

    # Queremos entre 2 e 4 números entre 1 e 30
    if baixos < 2 or baixos > 4:
        return False

    # Filtro inicial de soma
    if soma < 100 or soma > 260:
        return False

    return True


# ============================================================
# GERADOR ESTATÍSTICO COM FILTROS
# ============================================================

def gerar_com_filtros():

    tentativas = 0

    while tentativas < 10000:

        jogo = gerar_por_frequencia()

        if jogo_valido(jogo):
            return jogo

        tentativas += 1

    return gerar_aleatorio()


# ============================================================
# FORMATAR JOGO
# ============================================================

def mostrar_jogo(jogo):

    return " - ".join(
        f"{numero:02d}"
        for numero in jogo
    )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

print("\n========================================")
print("MEGADATA - GERADOR DE JOGOS")
print("========================================")

print("\nEscolha o método:")

print("1 - Aleatório")
print("2 - Frequência histórica")
print("3 - Estatístico com filtros")


opcao = input(
    "\nDigite a opção: "
)


if opcao == "1":

    jogo = gerar_aleatorio()

    metodo = "Aleatório"


elif opcao == "2":

    jogo = gerar_por_frequencia()

    metodo = "Frequência histórica"


elif opcao == "3":

    jogo = gerar_com_filtros()

    metodo = "Estatístico com filtros"


else:

    print("\nOpção inválida.")
    raise SystemExit


print("\n========================================")
print(f"MÉTODO: {metodo}")
print("========================================")

print(
    "\nJogo gerado:\n"
)

print(
    mostrar_jogo(jogo)
)

print(
    f"\nSoma: {sum(jogo)}"
)

print(
    "Pares:",
    sum(
        numero % 2 == 0
        for numero in jogo
    )
)

print(
    "Ímpares:",
    sum(
        numero % 2 != 0
        for numero in jogo
    )
)

print("\n========================================")
print(
    "Aviso: resultados anteriores não "
    "aumentam a probabilidade matemática "
    "de prever sorteios futuros."
)
print("========================================")