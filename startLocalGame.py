import subprocess

def open_script_in_new_window(script_path):
    subprocess.Popen(["start", "cmd", "/k", f"python {script_path}"], shell=True)

open_script_in_new_window("#debug.py")
open_script_in_new_window("#debug.py")
