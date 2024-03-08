from flask import Flask, request, jsonify, render_template

from tinydb import TinyDB

from models.Path import Path
from models.Point import Point

app = Flask(__name__)
db = TinyDB("caminhos.json")


@app.route("/paths", methods=["POST"])
def new_path():
    data = request.form
    if data is None or len(data) == 0:
        data = request.json

    name = data["name"]
    raw_points = data["points"]

    if isinstance(raw_points, str):
        raw_points = eval(raw_points)

    points = [
        Point(point.get("x"), point.get("y"), point.get("z"), point.get("r"))
        for point in raw_points
    ]
    path = Path(None, name, points)
    path.id = db.insert(path.to_dict())
    db.update({"id": path.id}, doc_ids=[path.id])
    return jsonify({"id": path.id})


@app.route("/paths/<id>", methods=["GET"])
def get_path(id):
    path = db.get(doc_id=int(id))
    return jsonify(path)


@app.route("/paths", methods=["GET"])
def get_all_paths():
    paths = db.all()
    return jsonify(paths)


@app.route("/update_path/<id>", methods=["PUT", "POST"])
def update(id):
    data = request.form
    if data is None or len(data) == 0:
        data = request.json

    name = data["name"]
    raw_points = data["points"]

    if isinstance(raw_points, str):
        raw_points = eval(raw_points)

    points = [
        Point(point.get("x"), point.get("y"), point.get("z"), point.get("r"))
        for point in raw_points
    ]

    path = Path(id, name, points)
    db.update(path.to_dict(), doc_ids=[int(id)])
    return jsonify({"id": path.id})


@app.route("/paths/<id>", methods=["DELETE"])
def delete(id):
    db.remove(doc_ids=[int(id)])
    return jsonify({"id": id})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/novo", methods=["GET"])
def novo():
    return render_template("new_path.html")


@app.route("/pegar_caminho/<id>", methods=["GET"])
def pegar_caminho(id):
    path = get_path(id).json
    return render_template("path.html", path=path)


@app.route("/listas_caminhos", methods=["GET"])
def listas_caminhos():
    paths = get_all_paths().json
    print(paths)
    return render_template("list_paths.html", paths=paths)


@app.route("/atualizar/<id>", methods=["GET"])
def atualizar(id):
    path = get_path(id).json
    return render_template("update_path.html", path=path)


@app.route("/deletar/<id>", methods=["GET"])
def deletar(id):
    delete(id)
    return render_template("delete_path.html", id=id)


if __name__ == "__main__":
    app.run(debug=True)
