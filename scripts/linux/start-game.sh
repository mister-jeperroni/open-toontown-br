#!/bin/sh
cd ..
cd ..
cd src/

export LOGIN_TOKEN=dev

python3 -m toontown.launcher.QuickStartLauncher --token $LOGIN_TOKEN
