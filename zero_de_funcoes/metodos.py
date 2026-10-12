def f(x):
    return (x**2) - 4

# Método Bissecção:
def metodo_bisseccao(a,b,tolerancia):
    print("MÉTODO DA BISSECÇÃO")

    print(f" intervalo [{a},{b}] |")

    #condições de aplicação:
    if f(a) * f(b) >= 0:
        print("Intervalo inválido")
        return

    while 1:
        #definir ponto médio
        x1 = (a + b)/2 
        print(f"Ponto médio = {x1}.\n")
        # verificar condições de parada
        if abs(f(x1)) <= tolerancia:
            print(f"Um zero da função é {x1}!\n")
            return

        # definir próximo intervalo
        if f(a) - f(x1) < 0:
            b = x1
        else:
            a = x1

        print(f" intervalo [{a},{b}] |")

# Método da Falsa Posição:


# Método do Newton-Raphson:


# Método da Secante:


# Testar Programa:
metodo_bisseccao(1,5,tolerancia=0)

