@echo off
:: -------------------------------
:: PyQt6 Project Folder Setup
:: Uses current directory as root
:: -------------------------------

:: Create source folders
mkdir src
mkdir src\widgets
mkdir src\layouts
mkdir src\utils

:: Create resource folders
mkdir resources
mkdir resources\icons
mkdir resources\styles

:: Create tests folder
mkdir tests

:: Create main files
echo from PyQt6.QtWidgets import QMainWindow > src\app_window.py
echo # Entry point > src\main.py
echo "" > tests\test_main.py
echo "" > resources\styles\style.qss
echo "" > resources\icons\readme.txt

:: Create project metadata files
echo # Requirements > requirements.txt
echo # Project README > README.md
echo "" > setup.py

echo.
echo PyQt6 project structure created in current directory: %CD%
pause