import time
import sympy as sp

# AUXILIARES
def criar_expressao(texto):
    x = sp.Symbol('x')
    expressao = sp.sympify(texto)
    return expressao    

def pegar_derivada(expressao):
    x = sp.Symbol('x')
    derivada = sp.diff(expressao,x)
    return derivada

# METODO DA BISSECCAO
def metodo_bisseccao(f, limiteA, limiteB, tolerancia, limite_iteracoes):

    inicio = time.perf_counter()

    # Validacao dos parametros
    if tolerancia <= 0:
        raise ValueError("A tolerancia deve ser positiva.")

    if limite_iteracoes < 1:
        raise ValueError("O limite de iteracoes deve ser positivo.")

    if limiteA >= limiteB:
        raise ValueError("O limiteA deve ser menor que limiteB.")

    fa = f(limiteA)
    fb = f(limiteB)

    raiz = None
    iteracoes = 0
    convergiu = False
    status = "Limite de iteracoes atingido"

    # Verifica se uma extremidade ja e uma raiz
    if fa == 0:
        raiz = limiteA
        convergiu = True
        status = "Raiz exata no limiteA"

    elif fb == 0:
        raiz = limiteB
        convergiu = True
        status = "Raiz exata no limiteB"

    # Verifica se existe mudanca de sinal
    elif fa * fb > 0:
        raise ValueError(
            "O intervalo nao apresenta mudanca de sinal."
        )

    else:
        # Loop principal da bisseccao
        for i in range(1, limite_iteracoes + 1):
            iteracoes = i

            # Calcula o ponto medio
            raiz = limiteA + (limiteB - limiteA) / 2

            fr = f(raiz)

            # Verifica a convergencia pelo residuo
            if abs(fr) <= tolerancia:
                convergiu = True
                status = "Convergencia pelo residuo"
                break

            # Atualiza o intervalo
            if fa * fr < 0:
                limiteB = raiz
                fb = fr
            else:
                limiteA = raiz
                fa = fr

    # Calcula o residuo final
    residuo = abs(f(raiz)) if raiz is not None else None

    fim = time.perf_counter()

    return {
        "metodo": "Bisseccao",
        "raiz": raiz,
        "iteracoes": iteracoes,
        "residuo": residuo,
        "convergiu": convergiu,
        "tempo_ms": (fim - inicio) * 1000,
        "status": status
    }

# Método falsa posição:
def metodo_falsa_pos(f, limiteA, limiteB, tolerancia, limite_iteracoes):

    inicio = time.perf_counter()

    # Validacao dos parametros
    if tolerancia <= 0:
        raise ValueError("A tolerancia deve ser positiva.")

    if limite_iteracoes < 1:
        raise ValueError("O limite de iteracoes deve ser positivo.")

    if limiteA >= limiteB:
        raise ValueError("O limiteA deve ser menor que limiteB.")

    fa = f(limiteA)
    fb = f(limiteB)

    raiz = None
    iteracoes = 0
    convergiu = False
    status = "Limite de iteracoes atingido"

    # Verifica se uma extremidade ja e uma raiz
    if fa == 0:
        raiz = limiteA
        convergiu = True
        status = "Raiz exata no limiteA"

    elif fb == 0:
        raiz = limiteB
        convergiu = True
        status = "Raiz exata no limiteB"

    # Verifica a mudanca de sinal
    elif fa * fb > 0:
        raise ValueError(
            "O intervalo nao apresenta mudanca de sinal."
        )

    else:
        # Loop principal da falsa posicao
        for i in range(1, limite_iteracoes + 1):
            iteracoes = i

            denominador = fb - fa

            if denominador == 0:
                raise ZeroDivisionError(
                    "Denominador nulo no metodo da falsa posicao."
                )

            # Calcula a nova aproximacao
            raiz = (limiteA * fb - limiteB * fa) / denominador

            fr = f(raiz)

            # Verifica a convergencia pelo residuo
            if abs(fr) <= tolerancia:
                convergiu = True
                status = "Convergencia pelo residuo"
                break

            # Atualiza o intervalo
            if fa * fr < 0:
                limiteB = raiz
                fb = fr
            else:
                limiteA = raiz
                fa = fr

    # Calcula o residuo final
    residuo = abs(f(raiz)) if raiz is not None else None

    fim = time.perf_counter()

    return {
        "metodo": "Falsa Posicao",
        "raiz": raiz,
        "iteracoes": iteracoes,
        "residuo": residuo,
        "convergiu": convergiu,
        "tempo_ms": (fim - inicio) * 1000,
        "status": status
    }

# METODO newton-Raphson:
def metodo_newton_raphson(f, df, x0, tolerancia, limite_iteracoes):

    inicio = time.perf_counter()

    # Validacao dos parametros
    if tolerancia <= 0:
        raise ValueError("A tolerancia deve ser positiva.")

    if limite_iteracoes < 1:
        raise ValueError("O limite de iteracoes deve ser positivo.")

    raiz = x0
    iteracoes = 0
    convergiu = False
    status = "Limite de iteracoes atingido"

    # Verifica se o chute inicial ja e uma raiz
    if abs(f(raiz)) <= tolerancia:
        convergiu = True
        status = "Convergencia pelo residuo"

    else:
        for i in range(1, limite_iteracoes + 1):
            iteracoes = i

            derivada = df(raiz)

            if derivada == 0:
                raise ZeroDivisionError(
                    "Derivada nula no metodo de Newton-Raphson."
                )

            # Calcula a proxima aproximacao
            nova_raiz = raiz - f(raiz) / derivada

            raiz = nova_raiz

            # Verifica a convergencia pelo residuo
            if abs(f(raiz)) <= tolerancia:
                convergiu = True
                status = "Convergencia pelo residuo"
                break

    residuo = abs(f(raiz))

    fim = time.perf_counter()

    return {
        "metodo": "Newton-Raphson",
        "raiz": raiz,
        "iteracoes": iteracoes,
        "residuo": residuo,
        "convergiu": convergiu,
        "tempo_ms": (fim - inicio) * 1000,
        "status": status
    }



# EXECUCAO DOS METODOS

def executar_metodos(
    texto_funcao,
    limiteA,
    limiteB,
    x0,
    tolerancia=1e-6,
    limite_iteracoes=1000
):
    # Cria a expressao simbolica
    expressao = criar_expressao(texto_funcao)

    # Converte a expressao para uma funcao numerica
    x = sp.Symbol('x')
    f = sp.lambdify(x, expressao, "math")

    # Calcula a derivada pra usar no newton RaPhson
    expressao_derivada = pegar_derivada(expressao)
    df = sp.lambdify(x, expressao_derivada, "math")

    resultados = []

    # Metodo da Bisseccao
    resultado = metodo_bisseccao(f, limiteA, limiteB, tolerancia, limite_iteracoes)
    resultados.append(resultado)

    # Metodo da Falsa Posicao
    resultado = metodo_falsa_pos(f, limiteA, limiteB, tolerancia, limite_iteracoes)
    resultados.append(resultado)

    resultado = metodo_newton_raphson(f, df, x0, tolerancia, limite_iteracoes)
    resultados.append(resultado)

    # Imprime os resultados
    print(f"\nFuncao analisada: {expressao}")
    print("\n========== RESULTADOS ==========")

    for resultado in resultados:
        print(f"\nMetodo: {resultado['metodo']}")
        print(f"Raiz encontrada: {resultado['raiz']}")
        print(f"Iteracoes: {resultado['iteracoes']}")
        print(f"Residuo final: {resultado['residuo']}")
        print(f"Convergiu: {resultado['convergiu']}")
        print(f"Tempo (ms): {resultado['tempo_ms']:.6f}")
        print(f"Status: {resultado['status']}")

    return resultados


# TESTE DO PROGRAMA
if __name__ == "__main__":

    texto = input("inserir f(x): ")

    dados = executar_metodos(
        texto_funcao = texto,
        limiteA=0,
        limiteB=8,
        x0 = 3,
        tolerancia=1e-6,
        limite_iteracoes=1000
    )

