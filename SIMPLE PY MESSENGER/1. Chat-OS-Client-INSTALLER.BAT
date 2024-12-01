@echo off

REM Download Python installer
curl -o python-installer.exe https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe

REM Install Python silently
start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

REM Add Python to PATH for the current session
setx path "%path%;C:\Python39;C:\Python39\Scripts"

REM Install pip if not already installed
python -m ensurepip --upgrade

REM Download Git installer
curl -o git-installer.exe https://github.com/git-for-windows/git/releases/download/v2.32.0.windows.1/Git-2.32.0-64-bit.exe

REM Install Git silently
start /wait git-installer.exe /SILENT

REM Install dependencies
python -m pip install kivy pillow pyautogui pyqt5

REM Clone the GitHub repository
git clone https://github.com/ryanrazzin/MESSAGING-PYTHON-APP.git

REM Change to the repository directory
cd yourrepository

echo Python, Git, app, and dependencies installed successfully.
pause
