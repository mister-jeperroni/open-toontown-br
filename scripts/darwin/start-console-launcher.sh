echo "Open Toontown - Console Launcher"
cd ..
cd ..
cd src/

# Read the contents of PPYTHON_PATH into PYTHON_PATH
if [ -f PPYTHON_PATH ]; then
    PYTHON_PATH=$(<PPYTHON_PATH)
else
    PYTHON_PATH=""
fi

# Set default value if PYTHON_PATH is empty
if [ -z "$PYTHON_PATH" ]; then
    PYTHON_PATH="python"
fi

$PYTHON_PATH -m launcher.ConsoleLauncher