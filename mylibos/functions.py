import json
import os, subprocess, psutil

def subprocess_bat(fp:str, shell=True):
    return subprocess.Popen(fp, shell=shell)

def terminate_process_by_pid(process:subprocess.Popen):
    if process:
        try:
            pid = process.pid
            if pid:
                proc = psutil.Process(pid)
                proc.terminate()
                proc.wait()
        except Exception as exc:
            return exc

def resource_load(fp: str):
    "This function returns the real path (like an './file.txt' or simple 'file.txt') of specified file"
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, fp)
    else:
        return os.path.join(os.path.abspath("."), fp)

def get_cpu_param_list():
    return ['all ', 'sd ', 'interrogate ', 'gfpgan ', 'bsrgan ', 'esrgan ', 'scunet ', 'codeformer ']

def get_args_for_start_webui():
    return ['--autolaunch', '--xformers', '--theme=dark', '--api', '--use-cpu ', '--medvram', '--listen']

def get_webui_batch_file_res(params:list) -> str:
    return f'''@echo off
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
set COMMANDLINE_ARGS= {params}
git pull origin master
call webui.bat'''

