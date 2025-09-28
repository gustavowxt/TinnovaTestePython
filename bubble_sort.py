def bubble_sort(vetor):
    n = len(vetor)
    V = vetor.copy()

    print(f"Vetor original: {', '.join(map(str, V))}\n")

    for i in range(n - 1):
        for j in range(n - i - 1):
            if V[j] > V[j + 1]:
                V[j], V[j + 1] = V[j + 1], V[j]
        print(f"Após iteração {i + 1}: {', '.join(map(str, V))}")

    print(f"\nVetor ordenado: {', '.join(map(str, V))}")


bubble_sort([5, 3, 2, 4, 7, 1, 0, 6])