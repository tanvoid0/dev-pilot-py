import subprocess

from py_helper.service.config_service import ConfigService

print("Configuring The project for the first time...")
# TODO: Install packages required by os first

# For windows
subprocess.run("python -m pip install -r requirements.txt")

# For Linux
subprocess.run("python3 -m pip install -r requirements.txt")

# TODO: add the os based apps from readme, here

ConfigService().first_time_setup()

print("Initiation completed. Run python dev-pilot.py")
