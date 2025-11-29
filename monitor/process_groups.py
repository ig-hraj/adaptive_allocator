import psutil

# Define your process groups here
PROCESS_GROUPS = {
    "batch_jobs": ["python", "notepad"],
    "interactive": ["chrome", "code"]
}

def get_group_usage():
    """Return CPU and memory usage per group"""
    group_usage = {}
    for group_name, names in PROCESS_GROUPS.items():
        cpu_total = 0
        mem_total = 0
        for proc in psutil.process_iter(['name', 'pid', 'cpu_percent', 'memory_percent']):
            if proc.info['name'] in names:
                cpu_total += proc.info['cpu_percent']
                mem_total += proc.info['memory_percent']
        group_usage[group_name] = {"cpu": cpu_total, "memory": mem_total}
    return group_usage

def adjust_priority(cpu_high, cpu_low, mem_high, mem_low):
    for group_name, names in PROCESS_GROUPS.items():
        for proc in psutil.process_iter(['name', 'pid', 'cpu_percent', 'memory_percent']):
            if proc.info['name'] in names:
                try:
                    p = psutil.Process(proc.info['pid'])
                    # CPU priority
                    if proc.info['cpu_percent'] > cpu_high:
                        p.nice(psutil.IDLE_PRIORITY_CLASS)
                    elif proc.info['cpu_percent'] < cpu_low:
                        p.nice(psutil.NORMAL_PRIORITY_CLASS)
                    # Memory priority
                    if proc.info['memory_percent'] > mem_high:
                        p.nice(psutil.IDLE_PRIORITY_CLASS)
                    elif proc.info['memory_percent'] < mem_low:
                        p.nice(psutil.NORMAL_PRIORITY_CLASS)
                except Exception as e:
                    print(f"Error adjusting {proc.info['name']}: {e}")
