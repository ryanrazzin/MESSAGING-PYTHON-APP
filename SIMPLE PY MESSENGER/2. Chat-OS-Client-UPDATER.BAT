@echo off

REM Update pip itself
python -m pip install --upgrade pip

REM Update specific dependencies
python -m pip install --upgrade kivy pillow pyautogui pyqt5

REM Define the URL for the latest project files (e.g., GitHub repository)
set REPO_URL=https://github.com/yourusername/yourrepository/archive/refs/heads/main.zip

REM Define the directory where the project is located
set PROJECT_DIR=C:\path\to\your\project

REM Download the latest project files
curl -L -o latest.zip %REPO_URL%

REM Unzip the latest project files (you need to have 7-Zip installed and added to your PATH)
7z x latest.zip -o%PROJECT_DIR% -aoa

REM Remove the downloaded zip file
del latest.zip

echo Dependencies and project files have been updated successfully.
pause
