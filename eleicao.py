class Eleicao:
    def __init__(self, total, validos, brancos, nulos):
        self.total = total
        self.validos = validos
        self.brancos = brancos
        self.nulos = nulos

    def percentual_validos(self):
        return (self.validos / self.total) * 100

    def percentual_brancos(self):
        return (self.brancos / self.total) * 100

    def percentual_nulos(self):
        return (self.nulos / self.total) * 100


eleicao = Eleicao(total=1000, validos=800, brancos=150, nulos=50)

print(f"Percentual de votos válidos: {eleicao.percentual_validos():.2f}%")
print(f"Percentual de votos brancos: {eleicao.percentual_brancos():.2f}%")
print(f"Percentual de votos nulos: {eleicao.percentual_nulos():.2f}%\n")

print("=== RESULTADOS ELEITORAIS ===")
print(f"Total de eleitores: {eleicao.total}")
print(f"Votos válidos: {eleicao.validos} ({eleicao.percentual_validos():.2f}%)")
print(f"Votos brancos: {eleicao.brancos} ({eleicao.percentual_brancos():.2f}%)")
print(f"Votos nulos: {eleicao.nulos} ({eleicao.percentual_nulos():.2f}%)")
print("=============================")