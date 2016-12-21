import os
import subprocess

all_files = os.listdir(os.getcwd())
py_files = [f for f in all_files if f.startswith("ex") and f.endswith(".py")]
py_files.sort()
for pf in py_files:
    print("-"*40)
    print("%s\n" % pf)
    if pf.startswith("ex09"):
        if (subprocess.call(["blender", "-b", "-P",  "./%s" % pf])):
            break
    else:
        if (subprocess.call(["python3",  "./%s" % pf])):
            break
