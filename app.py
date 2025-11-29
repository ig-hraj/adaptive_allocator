from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
from monitor.process_groups import get_group_usage, adjust_priority
import threading
import time

app = Flask(__name__)
CORS(app)

# Global thresholds
CPU_HIGH = 50
CPU_LOW = 10
MEM_HIGH = 70
MEM_LOW = 30

# Initialize CPU measurement
psutil.cpu_percent(interval=None)  # First call, returns 0.0 but initializes measurement

# Background thread to adjust priorities
def background_allocator():
    global CPU_HIGH, CPU_LOW, MEM_HIGH, MEM_LOW
    while True:
        adjust_priority(CPU_HIGH, CPU_LOW, MEM_HIGH, MEM_LOW)
        time.sleep(5)

threading.Thread(target=background_allocator, daemon=True).start()

@app.route("/monitor")
def monitor():
    cpu = psutil.cpu_percent(interval=0.5)  # Measure CPU usage over 0.5s
    memory = psutil.virtual_memory().percent
    group_usage = get_group_usage()
    return jsonify({
        "cpu_percent": cpu,
        "memory_percent": memory,
        "groups": group_usage
    })

@app.route("/set_thresholds", methods=["POST"])
def set_thresholds():
    global CPU_HIGH, CPU_LOW, MEM_HIGH, MEM_LOW
    data = request.json
    if "cpu_high" in data:
        CPU_HIGH = data["cpu_high"]
    if "cpu_low" in data:
        CPU_LOW = data["cpu_low"]
    if "mem_high" in data:
        MEM_HIGH = data["mem_high"]
    if "mem_low" in data:
        MEM_LOW = data["mem_low"]
    return jsonify({
        "message": "Thresholds updated",
        "cpu_high": CPU_HIGH, "cpu_low": CPU_LOW,
        "mem_high": MEM_HIGH, "mem_low": MEM_LOW
    })

if __name__ == "__main__":
    app.run(debug=True)
