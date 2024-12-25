import subprocess
import atexit
import time

processes = []

def openScript(path):
    global processes
    # Directly invoke Python without opening a new shell
    processes.append(subprocess.Popen(["python", path]))

def closeProcesses():
    global processes
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()

atexit.register(closeProcesses)

openScript("instant_host.py")

for i in range(4):
    openScript("instant_join.py")

while True:
    pass
