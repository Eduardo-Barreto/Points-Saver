"""
Para a questão prática da avaliação, você deve entregar um projeto Web implementado com o micro framework Flask em Python. Você deve criar um sistema Web que permita ao usuário realizar um cadastro dos pontos que o robô dele deve seguir. Cada conjunto de pontos que o robô for navegar, deve estar associado a um nome. Neste primeiro momento, o seu projeto deve realizar estas implementações para apenas um único usuário, portanto não existe a necessidade de realizar a diferenciação sobre o usuário que realizou o cadastro dos pontos.

O seu sistema deve, obrigatoriamente, utilizar o TinyDB para armazenar os dados. Eles devem ficar em um arquivo chamado caminhos.json. O usuário deve conseguir visualizar os caminhos que já foram cadastrados, modificar e deletar estes caminhos. Cada ponto armazenado deve ser representado por suas coordenadas: x, y, z e r. O seu sistema deve fornecer, no mínimo, as seguintes rotas:

●      /novo: cadastrar um novo conjunto de pontos em um caminho

●      /pegar_caminho: recebe o id do caminho e devolve os pontos cadastrados nele

●      /listas_caminhos: retorna o id e o nome de todos os caminhos cadastrados

●      /atualizar: atualiza o caminho cujo id foi fornecido

●      /deletar: deleta o caminho com o id fornecido

Outras rotas podem ser implementadas se a pessoa desenvolvedora julgar necessário.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

from tinydb import TinyDB, Query

db = TinyDB("caminhos.json")


class Point:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def to_dict(self):
        return {"x": self.x, "y": self.y, "z": self.z, "r": self.r}


class Path:
    def __init__(self, id, name, points):
        self.id = id
        self.name = name
        self.points = points

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "points": [point.to_dict() for point in self.points],
        }


@app.route("/novo", methods=["POST"])
def novo():
    data = request.json
    name = data["name"]
    raw_points = data["points"]
    points = [Point(*point) for point in raw_points]
    path = Path(None, name, points)
    path.id = db.insert(path.to_dict())
    db.update({"id": path.id}, doc_ids=[path.id])
    return jsonify({"id": path.id})


@app.route("/pegar_caminho", methods=["GET"])
def pegar_caminho():
    id = request.args.get("id")
    path = db.get(doc_id=int(id))
    return jsonify(path)


@app.route("/listas_caminhos", methods=["GET"])
def listas_caminhos():
    paths = db.all()
    return jsonify(paths)


@app.route("/atualizar", methods=["PUT"])
def atualizar():
    data = request.json
    id = data["id"]
    name = data["name"]
    points = [Point(*point) for point in data["points"]]
    path = Path(id, name, points)
    db.update(path.to_dict(), doc_ids=[int(id)])
    return jsonify({"id": path.id})


@app.route("/deletar", methods=["DELETE"])
def deletar():
    id = request.args.get("id")
    db.remove(doc_ids=[int(id)])
    return jsonify({"id": id})


if __name__ == "__main__":
    app.run(debug=True)
