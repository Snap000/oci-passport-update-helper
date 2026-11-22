@echo off
REM OCI Photo Prep - double-click me (Windows)
cd /d "%~dp0"
title OCI Photo Prep
set PY=
where py >nul 2>nul && set PY=py
if "%PY%"=="" (where python >nul 2>nul && set PY=python)
if "%PY%"=="" goto nopy
echo.
echo  Installing helper tools (first run only, about 1 minute)...
%PY% -m pip install --user -q -r requirements.txt
if errorlevel 1 goto pipfail
echo.
echo  Preparing your files...
%PY% scripts\oci_prep.py auto MyFiles
echo.
echo  Opening the MyFiles folder. Look inside each person's OCI_Ready folder.
explorer MyFiles
pause
exit /b

:nopy
echo.
echo  Python is not installed yet.
echo  1. The download page will open now. Install Python 3.
echo  2. IMPORTANT: tick "Add python.exe to PATH" on the first install screen.
echo  3. Double-click RUN-ME.bat again.
start https://www.python.org/downloads/
pause
exit /b

:pipfail
echo.
echo  Could not install the helper tools. Check your internet connection and try again.
pause
