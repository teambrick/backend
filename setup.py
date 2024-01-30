#pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org {i} for school

import os

with open("packages.txt", "r") as file:
    for i in file.read().split("\n"):
        # we can do it anyway
        cmd = f"pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org{i}"
        os.system(cmd)
