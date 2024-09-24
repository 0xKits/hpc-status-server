from flask import Flask
import psutil

app = Flask(__name__)

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds

def get_status():
    
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    temp = psutil.sensors_temperatures()
    up = get_uptime()

    return {
        "cpu": cpu, "mem": mem, "temp": temp, "uptime": up
    }

print(get_status())

@app.route("/status")
def status():
    return get_status()