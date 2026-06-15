import ipaddress
import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.get("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # FIX (CWE-78): validate the input, then run WITHOUT a shell and WITHOUT
    # string interpolation, so user input can never become a command.
    try:
        ipaddress.ip_address(host)          # only accept a literal IP
    except ValueError:
        return {"error": "host must be a valid IP address"}, 400

    result = subprocess.run(
        ["ping", "-c", "1", host],          # argument list, no shell=True
        capture_output=True, text=True, timeout=5,
    )
    return {"host": host, "output": result.stdout}
