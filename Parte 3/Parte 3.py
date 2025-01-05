class Aluno:
    def __init__(self, nome):
        self.nome = nome
        self.amizades = []
        self.atividades = []

    def adicionar_amizade(self, amigo):
        if amigo not in self.amizades:
            self.amizades.append(amigo)

    def adicionar_atividade(self, atividade):
        self.atividades.append(atividade)

class GestorTurma:
    def __init__(self):
        self.alunos = {}

    def adicionar_aluno(self, nome):
        if nome not in self.alunos:
            self.alunos[nome] = Aluno(nome)

    def remover_aluno(self, nome):
        if nome in self.alunos:
            # Remover o aluno da lista de amizades dos outros alunos
            for amigo in self.alunos[nome].amizades:
                self.alunos[amigo].amizades.remove(nome)
            del self.alunos[nome]

    def adicionar_amizade(self, nome1, nome2):
        if nome1 in self.alunos and nome2 in self.alunos:
            self.alunos[nome1].adicionar_amizade(nome2)
            self.alunos[nome2].adicionar_amizade(nome1)

    def adicionar_atividade(self, nome, atividade):
        if nome in self.alunos:
            self.alunos[nome].adicionar_atividade(atividade)

    def buscar_aluno(self, nome):
        return self.alunos.get(nome, None)

    def imprimir_estrutura(self):
        for nome, aluno in self.alunos.items():
            print(f"Aluno: {nome}")
            print(f"  Amizades: {aluno.amizades}")
            print(f"  Atividades: {aluno.atividades}")
            print()
