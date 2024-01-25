#pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org {i} for school

import os

with open("packages.txt", "r") as file:
    for i in file.read().split("\n"):
        cmd = f"pip install {i}"
        os.system(cmd)
