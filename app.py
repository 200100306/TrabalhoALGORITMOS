from flask import Flask, render_template, request, jsonify  # type: ignore

app = Flask(__name__)

# Estruturas de dados
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self, max_size):
        self.head = None
        self.size = 0
        self.max_size = max_size

    def add(self, data):
        if self.size >= self.max_size:
            return False
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
        return True

    def remove(self, data):
        if not self.head:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        if current.next:
            current.next = current.next.next
            self.size -= 1
            return True
        return False

    def pop(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return data

    def display(self):
        current = self.head
        students = []
        while current:
            students.append(current.data)  # Mantém todos os dados completos
            current = current.next
        return students

class HashTable:
    def __init__(self):
        self.table = {}

    def add(self, key, value):
        self.table[key] = value

    def remove(self, key):
        if key in self.table:
            del self.table[key]

    def display(self):
        return self.table

# Inicializando estruturas
turmas = {}  # Dicionário para armazenar turmas por letra
fila_espera = LinkedList(max_size=50)
informacoes_alunos = HashTable()

# Configuração inicial: primeira turma é "A"
turma_atual = "A"
turmas[turma_atual] = LinkedList(max_size=3)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json
    name = data.get("name")
    grade = data.get("grade")
    turma_letra = data.get("turma")

    # Validar nota
    if not (0 <= int(grade) <= 20):
        return jsonify({"message": "Erro: A nota deve estar entre 0 e 20."}), 400
    
    # Verificar se a turma já existe
    if turma_letra not in turmas:
        # Criar nova turma se não existir
        turmas[turma_letra] = LinkedList(max_size=3)

    # Tentar adicionar o aluno na turma
    if turmas[turma_letra].add(name):
        informacoes_alunos.add(name, {"notas": [grade], "turma": turma_letra})
        return jsonify({"message": f"Aluno adicionado à turma {turma_letra}!", "students": turmas[turma_letra].display()}), 200

    # Se a turma estiver cheia, adicionar o aluno à fila de espera
    fila_espera.add({"name": name, "turma": turma_letra, "grade": grade})
    return jsonify({"message": "Turma cheia. Aluno adicionado à fila de espera!", "queue": fila_espera.display()}), 200

@app.route("/remove_student", methods=["POST"])
def remove_student():
    name = request.json.get("name")
    for letra, turma in turmas.items():
        if turma.remove(name):
            informacoes_alunos.remove(name)
            # Verificar se há alunos na fila de espera
            if fila_espera.size > 0:
                next_in_line = fila_espera.pop()
                # Adicionar o aluno da fila à turma
                if turma.add(next_in_line["name"]):
                    # Atualizar as informações do aluno no hash table
                    informacoes_alunos.add(
                        next_in_line["name"],
                        {"notas": [next_in_line["grade"]], "turma": letra}
                    )
            return jsonify({
                "message": f"Aluno {name} removido com sucesso!",
                "students": turma.display(),
                "queue": fila_espera.display()
            }), 200
    return jsonify({"message": "Aluno não encontrado!"}), 404

@app.route("/data", methods=["GET"])
def get_data():
    all_students = {}
    for letra, turma in turmas.items():
        all_students[letra] = turma.display()
    return jsonify({
        "students": all_students,
        "queue": fila_espera.display(),  # Exibe os dados completos do aluno na fila de espera
        "info": informacoes_alunos.display(),
    })

if __name__ == "__main__":
    app.run(debug=True)
