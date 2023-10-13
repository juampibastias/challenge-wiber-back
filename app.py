from datetime import datetime
from bson import ObjectId
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config[
    "MONGO_URI"
] = "mongodb+srv://juanpedrobastiastorresi:nfqxYH6uOUUPRRDi@cluster0.yreqjlm.mongodb.net/mydatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route("/api/scripts", methods=["GET", "POST"])
def scripts():
    if request.method == "GET":
        scripts = mongo.db.scripts.find()
        return jsonify(
            [
                {
                    "id": str(script["_id"]),
                    "name": script["name"],
                    "text": script["text"],
                    "date": script.get("date", ""),
                    "time": script.get("time", ""),
                    "versions": script.get("versions", []),
                }
                for script in scripts
            ]
        )
    elif request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        text = data.get("text")
        # Obtener la fecha y la hora actuales en el servidor
        current_date_time = datetime.now()
        formatted_date = current_date_time.strftime("%d/%m/%y")
        formatted_time = current_date_time.strftime("%H:%M")
        new_script = {
            "name": name,
            "text": text,
            "date": formatted_date,
            "time": formatted_time,
            "versions": [],
        }
        mongo.db.scripts.insert_one(new_script)
        created_script = mongo.db.scripts.find_one(new_script)
        return (
            jsonify(
                {
                    "id": str(created_script["_id"]),
                    "name": created_script["name"],
                    "text": created_script["text"],
                    "date": created_script["date"],
                    "time": created_script["time"],
                    "versions": created_script["versions"],
                }
            ),
            201,
        )
    else:
        return jsonify({"error": "Método no permitido"}), 405


@app.route("/api/scripts/<string:script_id>", methods=["DELETE", "PUT"])
def script(script_id):
    if request.method == "DELETE":
        result = mongo.db.scripts.delete_one({"_id": ObjectId(script_id)})
        if result.deleted_count == 1:
            return jsonify({"message": "Script eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Script no encontrado"}), 404
    elif request.method == "PUT":
        data = request.get_json()
        updated_text = data["script"]
        # Obtener la fecha y la hora actuales en el servidor
        current_date_time = datetime.now()
        updated_date = current_date_time.strftime("%d/%m/%y")
        updated_time = current_date_time.strftime("%H:%M")
        mongo.db.scripts.update_one(
            {"_id": ObjectId(script_id)},
            {
                "$set": {
                    "text": updated_text,
                    "date": updated_date,  # Actualizar la fecha
                    "time": updated_time,  # Actualizar la hora
                },
            },
        )
        return jsonify({"message": "Script actualizado correctamente"}), 200


if __name__ == "__main__":
    app.run(debug=True)
