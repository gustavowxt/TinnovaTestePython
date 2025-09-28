def calculadora_multiplos():

    print("=== CALCULADORA DE MÚLTIPLOS DE 3 OU 5 ===\n")

    try:
        limite = int(input("Digite o limite: "))

        if limite <= 0:
            print("digite um número positivo.")
            return

        multiplos = []
        for numero in range(limite):
            if numero % 3 == 0 or numero % 5 == 0:
                multiplos.append(numero)

        # Mostra resultados
        print(f"\n--- Resultados para limite = {limite} ---")
        print(f"Múltiplos encontrados: {multiplos}")
        print(f"Quantidade de múltiplos: {len(multiplos)}")
        print(f"Soma total: {sum(multiplos)}")

    except ValueError:
        print("Erro: digite um número inteiro válido.")


calculadora_multiplos()