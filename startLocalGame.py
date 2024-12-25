import subprocess

def open_script_in_new_window(script_path):
    subprocess.Popen(["start", "cmd", "/k", f"python {script_path}"], shell=True)

for i in range(3):
    open_script_in_new_window("#debug.py")
