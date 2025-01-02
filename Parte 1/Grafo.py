class Grafo:
    def __init__(self):
        # Um dicionário onde as chaves são os vértices e os valores são listas de adjacências (vizinhos conectados por arestas)
        self.ligacao = {}
        self.amizades = []  # Lista para armazenar as amizades

    def adicionar_aluno(self, aluno):
        # Adiciona um vértice no grafo
        if aluno not in self.ligacao:
            self.ligacao[aluno] = []

    def adicionar_amizade(self, alunos):
        # Adiciona uma amizade (aresta) entre múltiplos alunos
        if all(aluno in self.ligacao for aluno in alunos):
            for aluno1 in alunos:
                for aluno2 in alunos:
                    if aluno1 != aluno2 and aluno2 not in self.ligacao[aluno1]:
                        self.ligacao[aluno1].append(aluno2)
                        self.amizades.append((aluno1, aluno2))

    def remover_aluno(self, aluno):
        # Remove um aluno do grafo
        if aluno in self.ligacao:
            # Remover o aluno da lista de adjacências de outros alunos
            for amigo in self.ligacao[aluno]:
                if aluno in self.ligacao[amigo]:
                    self.ligacao[amigo].remove(aluno)
            # Remover o aluno da lista de amizades
            self.amizades = [amizade for amizade in self.amizades if aluno not in amizade]
            # Remover o aluno do dicionário ligacao
            del self.ligacao[aluno]

    def imprimir(self):
        # Imprime o grafo
        for aluno in self.ligacao:
            print(aluno, ":", self.ligacao[aluno])
        
        # Imprime o número de amizades e os alunos dentro de cada amizade
        print("\nNúmero de amizades e os alunos dentro de cada amizade:")
        for i, (aluno1, aluno2) in enumerate(self.amizades, 1):
            print(f"Amizade {i}: {aluno1} e {aluno2}")

# Função principal
def main():
    grafo = Grafo()

    # Pedir ao utilizador que insira o número de alunos
    num_alunos = int(input("Insira o número de alunos na turma: "))

    # Criar uma lista para armazenar os nomes dos alunos
    nomes_alunos = input("Insira os nomes dos alunos separados por vírgulas: ").split(",")
    nomes_alunos = [nome.strip() for nome in nomes_alunos]  # Remover espaços extras

    # Adicionar os alunos ao grafo
    for nome in nomes_alunos:
        grafo.adicionar_aluno(nome)

    # Adicionar amizades entre os alunos utilizando a lista de nomes de alunos
    num_amizades = int(input("Insira o número de amizades na turma: "))
    for i in range(num_amizades):
        amizade = input(f"Insira os nomes dos alunos da amizade {i+1} separados por vírgula: ").split(",")
        amizade = [nome.strip() for nome in amizade]  # Remover espaços extras
        if len(amizade) > 1:
            grafo.adicionar_amizade(amizade)
        else:
            print(f"Entrada inválida para a amizade {i+1}")

    # Imprimir o grafo
    grafo.imprimir()

    # Remover um aluno
    aluno_remover = input("Insira o nome do aluno que deseja remover: ").strip()
    grafo.remover_aluno(aluno_remover)

    # Imprimir o grafo após a remoção
    print("\nGrafo após a remoção do aluno:")
    grafo.imprimir()

# Executar a função principal
if __name__ == "__main__":
    main()
