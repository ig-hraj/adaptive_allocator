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
# -------------------------------------------------------------
# BACKGROUND THREAD: Adaptive Allocator + Uptime Logging
# -------------------------------------------------------------
def background_allocator():
    global CPU_HIGH, CPU_LOW, MEM_HIGH, MEM_LOW
    while True:
        # Adjust process group priorities
        adjust_priority(CPU_HIGH, CPU_LOW, MEM_HIGH, MEM_LOW)

        # Get CPU and memory usage
        cpu = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory().percent

        # Calculate system uptime
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)

        # Print status in console
        print(f"[STATUS] CPU: {cpu}% | Memory: {memory}% | Uptime: {hours}h {minutes}m {seconds}s")

        # Sleep for 5 seconds before next check
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
# ROUTE: /uptime
# Returns the system uptime in seconds and a human-readable format
# -------------------------------------------------------------
@app.route("/uptime")
def get_uptime():
    boot_time = psutil.boot_time()  # system boot time in seconds since epoch
    uptime_seconds = time.time() - boot_time

    # Convert to hours, minutes, seconds
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)

    return jsonify({
        "uptime_seconds": int(uptime_seconds),
        "uptime": f"{hours}h {minutes}m {seconds}s"
    })


# -------------------------------------------------------------
# MAIN ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
