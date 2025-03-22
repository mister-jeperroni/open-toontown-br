@echo off
title Toontown BR QA- Game Client
cd..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

set LOGIN_TOKEN=dev

%PPYTHON_PATH% -m dumped.toontown.launcher.StartToontownLauncher
pause
