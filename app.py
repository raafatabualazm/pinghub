import os
from flask import Flask, request

app = Flask(__name__)

# The real token is read from the environment at runtime...
API_TOKEN = os.environ.get("API_TOKEN", "")


@app.get("/")
def health():
    return {"service": "pinghub", "status": "ok"}


@app.get("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # PLANTED VULN (CWE-78 Command Injection):
    # user input is interpolated straight into a shell command.
    #   /ping?host=8.8.8.8
    #   /ping?host=8.8.8.8;%20cat%20/etc/passwd
    output = os.popen(f"ping -c 1 {host}").read()
    return {"host": host, "output": output}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
