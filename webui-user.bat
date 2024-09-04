@echo off
if not exist python (echo Unpacking Git and Python... & mkdir tmp & start /wait git_python.part01.exe & del git_python.part01.exe & del git_python.part*.rar)
set pypath=home = %~dp0python
if exist venv (powershell -command "$text = (gc venv\pyvenv.cfg) -replace 'home = .*', $env:pypath; $Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding($False);[System.IO.File]::WriteAllLines('venv\pyvenv.cfg', $text, $Utf8NoBomEncoding);")

set APPDATA=tmp
set USERPROFILE=tmp
set TEMP=tmp
set PYTHON=python\python.exe
set GIT=git\cmd\git.exe
set PATH=git\cmd
set VENV_DIR=venv
set COMMANDLINE_ARGS= --autolaunch --xformers --theme=dark --use-cpu=all --listen 
git pull origin master
call webui.bat