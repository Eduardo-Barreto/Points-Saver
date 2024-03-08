from flask import Flask, request, jsonify

from tinydb import TinyDB, Query

from models.Path import Path
from models.Point import Point

app = Flask(__name__)
db = TinyDB("caminhos.json")


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
