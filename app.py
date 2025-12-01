"""
---------------------------------------------------------------
 Adaptive Resource Allocation System - Backend (Flask API)
---------------------------------------------------------------
 This backend continuously monitors the system's CPU and Memory
 usage and sends the data to the frontend dashboard.

 It also contains a background allocator thread that automatically
 adjusts the priority of process groups based on thresholds
 set by the user from the dashboard.
---------------------------------------------------------------
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import threading
import time

# Import custom resource management logic
from monitor.process_groups import get_group_usage, adjust_priority

app = Flask(__name__)
CORS(app)

# -------------------------------------------------------------
# GLOBAL THRESHOLDS (Default Values)
# These values can be changed dynamically via /set_thresholds
# -------------------------------------------------------------
CPU_HIGH = 50
CPU_LOW = 10
MEM_HIGH = 70
MEM_LOW = 30

# -------------------------------------------------------------
# Initialize CPU tracking so that subsequent calls give
# accurate readings.
# -------------------------------------------------------------
psutil.cpu_percent(interval=None)


# -------------------------------------------------------------
# BACKGROUND THREAD: Adaptive Allocator
# This thread automatically adjusts process group priorities
# based on the defined thresholds.
# Runs every 5 seconds in the background.
# -------------------------------------------------------------
def background_allocator():
    global CPU_HIGH, CPU_LOW, MEM_HIGH, MEM_LOW
    while True:
        adjust_priority(CPU_HIGH, CPU_LOW, MEM_HIGH, MEM_LOW)
        time.sleep(5)


# Start the allocator thread in daemon mode
threading.Thread(target=background_allocator, daemon=True).start()


# -------------------------------------------------------------
# ROUTE: /monitor
# Returns:
#   - Live CPU Percent
#   - Live Memory Percent
#   - Group-wise resource usage
# Used by frontend for real-time dashboard updates.
# -------------------------------------------------------------
@app.route("/monitor")
def monitor():
    cpu = psutil.cpu_percent(interval=0.5)  # More accurate sampling
    memory = psutil.virtual_memory().percent
    group_usage = get_group_usage()

    return jsonify({
        "cpu_percent": cpu,
        "memory_percent": memory,
        "groups": group_usage
    })


# -------------------------------------------------------------
# ROUTE: /set_thresholds
# Allows frontend to update:
#   - CPU_HIGH, CPU_LOW
#   - MEM_HIGH, MEM_LOW
#
# Returns updated values for confirmation.
# -------------------------------------------------------------
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
        "message": "Thresholds updated successfully",
        "cpu_high": CPU_HIGH,
        "cpu_low": CPU_LOW,
        "mem_high": MEM_HIGH,
        "mem_low": MEM_LOW
    })


# -------------------------------------------------------------
# MAIN ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
