import platform
import subprocess

os_name = platform.system()
print(f"Configuring The project for the first time for {os_name}...")
# TODO: Install packages required by os first

# For windows
python_command = "python"
# For Linux
if os_name == 'Linux' or os_name == 'Darwin':
    python_command = "python3"
subprocess.run(f"{python_command} -m pip install --upgrade pip")
subprocess.run(f"{python_command} -m pip install -r requirements.txt")

# TODO: add the os based apps from readme, here

from py_helper.service.config_service import ConfigService

ConfigService().first_time_setup()

print("Initiation completed. Run python dev-pilot.py")
