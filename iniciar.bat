@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py
if not exist .venv\Scripts\python.exe %PY% -m venv .venv
if not exist .venv\Scripts\python.exe (
  echo No se encontro Python 3. Instalalo desde https://www.python.org/downloads/ marcando "Add python.exe to PATH".
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m pip install -q -r requirements.txt
.venv\Scripts\python.exe run.py %*
pause
