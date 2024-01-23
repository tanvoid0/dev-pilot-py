# Required Libraries

## Python

install python libraries - `pip install -r requirements.txt`

## Windows
Windows should be ready to test as long as you have python and ran the python library installation
Please do report if you find anything missing.

## Linux

gnome-terminal - `sudo apt-get install gnome-terminal`

permit scripts - `sudo chmod +x pilot.py, exec.sh, dev-pilot.py`

tkinter - `sudo apt-get install python3-tk`

pyqt - `sudo apt-get install python3-pyqt5`

cursor `sudo apt install xcb-cursor0`

## Work List

- [x] Autopilot
- [x] Deployment Viewer
- [x] String command generator
- [ ] First Time setup runner
- [ ] Reorder Deployments
- [ ] Configure image tag
- [ ] Notification

## Plan out

- [ ] How to work with Sync terminal, and capture the output for validation
- [ ] Progress Stepper
- [ ] Kubernetes
  - [ ] show pod logs
  - [x] show pod status
  - [x] Reorder deployments & statefulsets
- [ ] Reorder Project
