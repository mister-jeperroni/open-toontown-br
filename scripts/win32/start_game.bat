@echo off
title Open Toontown - Game Client
cd ..
cd ..
cd src

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH
rem Set default value if PPYTHON_PATH is empty:
if "%PPYTHON_PATH%"=="" set PPYTHON_PATH=python

set LOGIN_TOKEN=dev

%PPYTHON_PATH% -m toontown.launcher.QuickStartLauncher
pause
