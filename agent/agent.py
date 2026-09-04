import psutil
import platform
import socket
import time
import requests
from datetime import datetime


BACKEND_URL = "http://127.0.0.1:8000/metrics/"

previous_processes = {}


def collect_processes():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "status", "memory_percent", "create_time"]
    ):
        try:
            cpu_percent = process.cpu_percent(interval=0.1)

            info = process.info

            # Ignore Windows System Idle Process
            if info["name"] == "System Idle Process":
                continue

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "status": info["status"],
                "create_time": info["create_time"],
                "cpu_usage": round(cpu_percent, 2),
                "memory_usage": round(
                    info["memory_percent"] or 0,
                    2
                ),
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return processes


def detect_process_changes(current_processes):
    global previous_processes

    current_process_map = {}

    for process in current_processes:
        key = (
            process["pid"],
            process["name"],
            process["create_time"]
        )

        current_process_map[key] = process

    previous_keys = set(previous_processes.keys())
    current_keys = set(current_process_map.keys())

    started_keys = current_keys - previous_keys
    stopped_keys = previous_keys - current_keys

    started = [
        current_process_map[key]
        for key in started_keys
    ]

    stopped = [
        previous_processes[key]
        for key in stopped_keys
    ]

    previous_processes = current_process_map

    return {
        "started": started,
        "stopped": stopped,
    }


def collect_metrics():
    processes = collect_processes()

    process_changes = detect_process_changes(processes)

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "timestamp": datetime.now().isoformat(),

        "cpu_usage": psutil.cpu_percent(interval=1),

        "memory_usage": psutil.virtual_memory().percent,

        "disk_usage": psutil.disk_usage("C:\\").percent,

        "processes": processes,

        "process_changes": process_changes,
    }


def print_metrics(metrics):
    print("\n" + "=" * 65)
    print("AEGIS AGENT - REAL SYSTEM METRICS")
    print("=" * 65)

    print(f"Hostname: {metrics['hostname']}")
    print(f"OS: {metrics['os']}")
    print(f"CPU: {metrics['cpu_usage']}%")
    print(f"Memory: {metrics['memory_usage']}%")
    print(f"Disk: {metrics['disk_usage']}%")

    print("\nProcess Changes:")
    print("-" * 65)

    started = metrics["process_changes"]["started"]
    stopped = metrics["process_changes"]["stopped"]

    if started:
        print("STARTED:")
        for process in started:
            print(
                f"  + {process['name']} "
                f"(PID: {process['pid']})"
            )

    if stopped:
        print("STOPPED:")
        for process in stopped:
            print(
                f"  - {process['name']} "
                f"(PID: {process['pid']})"
            )

    if not started and not stopped:
        print("No process changes detected.")

    print("\nRunning Processes:")
    print("-" * 65)

    for process in metrics["processes"][:20]:
        print(
            f"{process['pid']:>6} | "
            f"{process['name']:<30} | "
            f"{process['status']:<10} | "
            f"CPU: {process['cpu_usage']:>6}% | "
            f"RAM: {process['memory_usage']:>6}%"
        )

    print(
        f"\nTotal processes: "
        f"{len(metrics['processes'])}"
    )


def send_metrics(metrics):
    try:
        response = requests.post(
            BACKEND_URL,
            json=metrics,
            timeout=5
        )

        print("\nBackend response:")
        print(response.status_code)
        print(response.json())

    except requests.exceptions.RequestException as error:
        print("\nFailed to send metrics:")
        print(error)


if __name__ == "__main__":
    print("AEGIS Agent started...")
    print("Monitoring system every 10 seconds.")
    print("Press Ctrl + C to stop.")

    try:
        while True:
            metrics = collect_metrics()

            print_metrics(metrics)

            send_metrics(metrics)

            time.sleep(10)

    except KeyboardInterrupt:
        print("\nAEGIS Agent stopped.")