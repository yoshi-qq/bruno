import subprocess
import sys
import time
import atexit
import os

name = "#test_game.py"
processes = []

def runSelfAsSubprocess(host=False):
    args = [sys.executable, name]
    if host:
        args.append("--host")
    else:
        args.append("--join")
    process = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr)
    processes.append(process)
    return process

def close_processes():
    for process in processes:
        if process.poll() is None:
            process.terminate()
            process.wait()
    print("All subprocesses closed.")

atexit.register(close_processes)

def instant_host():
    import time
    from scripts.main import init, start
    from scripts.config.constants import DEFAULT_IP, DEFAULT_PORT
    from scripts.utils.menuing import hostButton
    from scripts.utils.gameLogic import startGame

    def host():
        hostButton(DEFAULT_IP, DEFAULT_PORT)

    init()
    host()
    time.sleep(1.5)
    startGame()
    start()

def instant_join():
    from scripts.main import init, start
    from scripts.config.constants import DEFAULT_IP, DEFAULT_PORT
    from scripts.utils.menuing import joinButton

    def intercept():
        joinButton(DEFAULT_IP, DEFAULT_PORT)

    init()
    intercept()
    start()

if __name__ == "__main__":
    if "--host" in sys.argv:
        print("Host started")
        instant_host()
    elif "--join" in sys.argv:
        print("Player started")
        instant_join()
    else:
        print("Main started")

        host_process = runSelfAsSubprocess(host=True)
        time.sleep(0.5)

        join_processes = [runSelfAsSubprocess() for _ in range(4)]

        host_process.wait()
        for join_process in join_processes:
            join_process.wait()

        print("Main finished")