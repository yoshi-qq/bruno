import subprocess, atexit, os, signal

processes = []

def openScript(path):
    processes.append(subprocess.Popen(["start", "cmd", "/k", f"python {path}"], shell=True))

openScript("instant_host.py")

for i in range(3):
    openScript("instant_join.py")

def closeProcesses():
    for process in processes:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

atexit.register