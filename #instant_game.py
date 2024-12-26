import subprocess, atexit, os, signal

processes = []

def openScript(path):
    processes.append(subprocess.Popen(
        ["python", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
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