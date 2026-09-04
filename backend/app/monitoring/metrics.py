import psutil

from prometheus_client import Gauge


cpu_usage = Gauge(
    "aegis_cpu_usage_percent",
    "Current CPU usage percentage"
)

memory_usage = Gauge(
    "aegis_memory_usage_percent",
    "Current memory usage percentage"
)

disk_usage = Gauge(
    "aegis_disk_usage_percent",
    "Current disk usage percentage"
)

network_sent = Gauge(
    "aegis_network_bytes_sent",
    "Total network bytes sent"
)

network_received = Gauge(
    "aegis_network_bytes_received",
    "Total network bytes received"
)


def update_system_metrics():

    cpu = psutil.cpu_percent(interval=0.1)

    memory = psutil.virtual_memory().percent

    disk_path = "C:\\" if psutil.WINDOWS else "/"
    disk = psutil.disk_usage(disk_path).percent

    network = psutil.net_io_counters()

    sent = network.bytes_sent
    received = network.bytes_recv

    cpu_usage.set(cpu)
    memory_usage.set(memory)
    disk_usage.set(disk)

    network_sent.set(sent)
    network_received.set(received)

    return {
        "cpu_usage": cpu,
        "memory_usage": memory,
        "disk_usage": disk,
        "network_sent": sent,
        "network_received": received,
    }


def collect_processes():

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "status",
            "memory_percent",
            "create_time",
        ]
    ):

        try:

            info = process.info

            if info["name"] == "System Idle Process":
                continue

            cpu_percent = process.cpu_percent(interval=0.05)

            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"],
                    "status": info["status"],
                    "cpu_usage": round(cpu_percent, 2),
                    "memory_usage": round(
                        info["memory_percent"] or 0,
                        2
                    ),
                    "create_time": info["create_time"],
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return processes


def get_monitoring_snapshot():

    system_metrics = update_system_metrics()

    processes = collect_processes()

    return {
        "cpu_usage": system_metrics["cpu_usage"],
        "memory_usage": system_metrics["memory_usage"],
        "disk_usage": system_metrics["disk_usage"],
        "network_sent": system_metrics["network_sent"],
        "network_received": system_metrics["network_received"],
        "processes": processes,
        "process_count": len(processes),
    }