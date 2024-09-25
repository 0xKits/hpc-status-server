from flask import Flask
import gpustat
import psutil

app = Flask(__name__)


def get_uptime():
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds


def get_status():

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    temp = psutil.sensors_temperatures()
    up = get_uptime()
    gpu = (gpustat.new_query().jsonify())["gpus"][0]
    print(gpu["name"], gpu["utilization.gpu"], gpu["memory.used"], gpu["memory.total"])

    return {
        "cpu": cpu,
        "mem": mem,
        "temp": {"cpu": temp["k10temp"][0][1], "gpu": gpu["temperature.gpu"]},
        "uptime": up,
        "gpu": {
            "name": gpu["name"],
            "util": gpu["utilization.gpu"],
            "mem": gpu["memory.total"]
        },
    }


@app.route("/status")
def status():
    return get_status()
