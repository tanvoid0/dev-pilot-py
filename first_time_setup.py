import subprocess

from py_helper.service.config_service import ConfigService

print("Configuring The project for the first time...")
# TODO: Install packages required by os first

subprocess.run("python -m pip install -r requirements.txt")
ConfigService().first_time_setup()

print("Initiation completed. Run python dev-pilot.py")
