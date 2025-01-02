from flask import Flask, render_template, request, jsonify # type: ignore

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

    def display(self):
        current = self.head
        students = []
        while current:
            students.append(current.data)
            current = current.next
        return students

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.items:
            return self.items.pop(0)
        return None

    def display(self):
        return self.items

class HashTable:
    def __init__(self):
        self.table = {}

    def add(self, key, value):
        self.table[key] = value

    def remove(self, key):
        if key in self.table:
            del self.table[key]

    def update(self, key, field, value):
        if key in self.table:
            self.table[key][field] = value

    def display(self):
        return self.table

# Inicializando estruturas
turma = LinkedList(max_size=3)
fila_espera = Queue()
informacoes_alunos = HashTable()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json
    name = data.get("name")
    turma_name = data.get("turma")
    grade = data.get("grade")
    if turma.add(name):
        informacoes_alunos.add(name, {"notas": [grade], "status": "matriculado", "turma": turma_name})
        return jsonify({"message": "Aluno matriculado!", "students": turma.display()}), 200
    else:
        fila_espera.enqueue(name)
        return jsonify({"message": "Turma cheia, aluno adicionado à fila de espera!", "queue": fila_espera.display()}), 200

@app.route("/remove_student", methods=["POST"])
def remove_student():
    name = request.json.get("name")
    if turma.remove(name):
        informacoes_alunos.remove(name)
        return jsonify({"message": f"Aluno {name} removido da turma!", "students": turma.display()}), 200
    return jsonify({"message": "Aluno não encontrado na turma!"}), 404

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify({
        "students": turma.display(),
        "queue": fila_espera.display(),
        "info": informacoes_alunos.display()
    })

if __name__ == "__main__":
    app.run(debug=True)
