import argparse
import os
import sys
import traceback
import logging
from panda3d.core import loadPrcFile
from toontown.launcher.QuickLauncher import QuickLauncher

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(
    filename=os.path.join(log_dir, "toontown.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

try:
    parser = argparse.ArgumentParser(description="Open Toontown - Quick Launcher")
    parser.add_argument("--token", help="The token that the server will use.")
    args = parser.parse_args()

    if args.token:
        os.environ["LOGIN_TOKEN"] = args.token
    else:
        os.environ["LOGIN_TOKEN"] = "dev"
        logging.info("Usando token padrão: dev")
    loadPrcFile("../config/Configrc.prc")
    launcher = QuickLauncher()
    launcher.notify.info("Reached end of main.py.")

except Exception as e:
    logging.critical(f"Erro fatal ao iniciar: {e}")
    logging.critical(traceback.format_exc())

    if getattr(sys, "frozen", False):
        try:
            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Erro ao iniciar Open Toontown BR",
                f"Ocorreu um erro ao iniciar o jogo: {e}\n\nPor favor, verifique o arquivo de log em 'logs/toontown.log'.",
            )
        except:
            pass

    sys.exit(1)
