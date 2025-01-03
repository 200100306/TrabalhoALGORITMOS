from flask import Flask, render_template, request, jsonify  # type: ignore


app = Flask(__name__)

# Estruturas de dados
class No:
    def __init__(self, nome):
        self.nome = nome
        self.tutor = None
        self.filhos = []

class Arvore:
    def __init__(self):
        self.nos = {}

    def adicionar_pessoa(self, nome):
        """Adiciona uma pessoa (aluno ou tutor) à árvore."""
        if nome not in self.nos:
            self.nos[nome] = No(nome)

    def adicionar_tutor(self, nome_aluno, nome_tutor):
        """Associa um tutor a um aluno."""
        if nome_aluno in self.nos:
            if nome_tutor not in self.nos:
                self.adicionar_pessoa(nome_tutor)
            aluno = self.nos[nome_aluno]
            tutor = self.nos[nome_tutor]
            aluno.tutor = tutor
            if aluno not in tutor.filhos:
                tutor.filhos.append(aluno)

    def imprimir(self):
        """Imprime a árvore de forma agrupada por tutor."""
        print("\nEstrutura da árvore de tutores:")
        for nome, no in self.nos.items():
            if no.filhos:  # Tutores com filhos
                print(f"Tutor: {nome}")
                for filho in no.filhos:
                    print(f"  - {filho.nome}")
            elif no.tutor is None:  # Pessoas sem tutor
                print(f"Tutor: {nome} (Sem alunos)")

def main():
    arvore = Arvore()

    # Inserir tutores
    num_tutores = int(input("Insira o número de tutores: "))
    for _ in range(num_tutores):
        nome = input("Insira o nome do tutor: ").strip()
        arvore.adicionar_pessoa(nome)

    # Inserir alunos
    num_alunos = int(input("\nInsira o número de alunos: "))
    for _ in range(num_alunos):
        nome = input("Insira o nome do aluno: ").strip()
        arvore.adicionar_pessoa(nome)

    # Associar alunos a tutores
    print("\nAgora, associe os alunos aos tutores:")
    for _ in range(num_alunos):
        nome_aluno = input("Nome do aluno: ").strip()
        nome_tutor = input(f"Nome do tutor para {nome_aluno}: ").strip()
        arvore.adicionar_tutor(nome_aluno, nome_tutor)

    # Exibir a árvore
    arvore.imprimir()

if __name__ == "__main__":
    main()


@app.route("/tree")
def tree_page():
    return render_template("tree.html")
