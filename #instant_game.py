import subprocess, atexit, os, signal

processes = []

debug = False

def openScript(path):
    if debug:
        processes.append(subprocess.Popen(["start", "cmd", "/k", f"python {path}"], shell=True))
    else:
        processes.append(subprocess.Popen(
            ["python", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ))

openScript("instant_host.py")

for i in range(4):
    openScript("instant_join.py")

def closeProcesses():
    for process in processes:
        os.kill(process)

atexit.register(closeProcesses)

while True:
    pass