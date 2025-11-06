# server.py - Virtual Voice-Controlled ESP32 Simulation

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Simulated ESP32 device state
aps = {"AP1": False, "AP2": False, "AP3": True, "AP4": True}

@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "client.html")

@app.route("/status", methods=["GET"])
def status():
    return jsonify(aps)

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(force=True)
    cmd = data.get("command", "").lower()
    print(f"Received command: {cmd}")

    if cmd == "on all":
        for k in aps: aps[k] = True
    elif cmd == "off all":
        for k in aps: aps[k] = False
    elif cmd.startswith("on "):
        ap = cmd.split(" ")[1].upper()
        if ap in aps: aps[ap] = True
    elif cmd.startswith("off "):
        ap = cmd.split(" ")[1].upper()
        if ap in aps: aps[ap] = False

    print(f"Updated state: {aps}")
    return jsonify({"ok": True, "state": aps})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
