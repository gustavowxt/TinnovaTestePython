def calcular_fatorial():

    print("=== CALCULADORA DE FATORIAL ===")

    try:
        numero = int(input("Digite um número inteiro não negativo: "))

        if numero < 0:
            print("Erro: O fatorial só está definido para números não negativos.")
            return

        resultado = 1
        expressao = ""

        for i in range(numero, 0, -1):
            resultado *= i
            if i > 1:
                expressao += f"{i} × "
            else:
                expressao += f"{i}"

        print(f"\n{numero}! = {expressao} = {resultado}")

    except ValueError:
        print("Erro: Por favor, digite um número inteiro válido.")

calcular_fatorial()