#!/bin/sh
cd ..
cd ..

export LOGIN_TOKEN=dev

/usr/local/bin/python3.9 -m toontown.launcher.QuickStartLauncher --token $LOGIN_TOKEN
