from flask import Flask, jsonify, request
from flask_cors import CORS
from env import SupportTicketEnv

app = Flask(__name__)
CORS(app)

env = SupportTicketEnv()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "OpenEnv Support Ticket Classifier is running",
        "status": "ok"
    }), 200


@app.route("/reset", methods=["GET", "POST"])
def reset_env():
    return jsonify(env.reset()), 200


@app.route("/state", methods=["GET", "POST"])
def get_state():
    return jsonify(env.state()), 200


@app.route("/step", methods=["POST"])
def step_env():
    data = request.get_json(silent=True)

    if not data or "action" not in data:
        return jsonify({"error": "Missing 'action' in request body"}), 400

    return jsonify(env.step(data["action"])), 200


@app.route("/auto_step", methods=["POST"])
def auto_step():
    action = env.auto_action()
    result = env.step(action)
    result["auto_action"] = action
    return jsonify(result), 200


print("app.py loaded")


if __name__ == "__main__":
    print("starting flask server...")
    app.run(host="0.0.0.0", port=7860, debug=True)
