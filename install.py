# makes sure prerequisites are already installed
import os
import utils.system_utils as system

system.printSystemInfo()

pip3Path = os.getenv('PIP3')
if not pip3Path:
    print("PIP3 environment variable not set")
    cmd = ['which', 'pip3']
    pip3Path = system.runCommand(cmd)

pip3Path = pip3Path.strip()

if not pip3Path:
    print("pip3 path not found")
    exit()

try:
    import requests
    print("package requests already installed")
except:
    system.pipInstall('requests')

try:
    import pandas
    print("package pandas already installed")
except:
    system.pipInstall('pandas')

system.runNodeCommand(['npm', 'i'])

print("Install Success")
