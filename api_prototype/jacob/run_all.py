import os
import subprocess

all_files = os.listdir(os.getcwd())
py_files = [f for f in all_files if f.startswith("ex") and f.endswith(".py")]
py_files.sort()
for pf in py_files:
    print("-"*40)
    print("%s\n" % pf)
    subprocess.call(["python3",  "./%s" % pf])
