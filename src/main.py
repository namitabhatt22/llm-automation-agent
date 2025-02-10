from flask import Flask, request, jsonify
import os
from tasks import execute_task

app = Flask(__name__)

DATA_DIR = "/data"

@app.route("/run", methods=["POST"])
def run_task():
    data = request.get_json()
    task = data.get("task", "").strip() if data else ""

    if not task:
        return jsonify({"error": "No task description provided"}), 400

    try:
        output_path = execute_task(task)
        if output_path:
            return jsonify({"message": "Task executed successfully", "output_path": output_path}), 200
        return jsonify({"error": "Task execution failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/read", methods=["GET"])
def read_file():
    path = request.args.get("path", "").strip()
    full_path = os.path.join(DATA_DIR, path.lstrip("/"))

    if not full_path.startswith(DATA_DIR):
        return jsonify({"error": "Access outside /data is prohibited"}), 403

    if not os.path.exists(full_path):
        return "", 404

    with open(full_path, "r") as f:
        content = f.read()

    return content, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
