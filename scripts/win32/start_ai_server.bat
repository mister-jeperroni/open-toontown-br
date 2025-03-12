@echo off
title Open Toontown - AI (District) Server
cd ..
cd ..
cd src/

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH
rem Set default value if PPYTHON_PATH is empty:
if "%PPYTHON_PATH%"=="" set PPYTHON_PATH=python

:main
%PPYTHON_PATH% -m toontown.ai.AIStart --base-channel 401000000 ^
               --max-channels 999999 --stateserver 4002 ^
               --messagedirector-ip 127.0.0.1:7199 ^
               --eventlogger-ip 127.0.0.1:7197 ^
               --district-name "Toon Valley"
goto main
