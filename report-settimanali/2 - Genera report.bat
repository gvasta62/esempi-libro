@echo off
title Genera report settimanale
for /f "delims=" %%i in ('wsl.exe wslpath -a "%~dp0genera_report.sh"') do set SCRIPT=%%i
wsl.exe bash -lc "bash '%SCRIPT%'"
