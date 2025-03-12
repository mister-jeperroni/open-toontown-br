import subprocess
import os
import sys
import time

from api.ApiConnector import ApiConnector

class LauncherProcess:
    def __init__(self):
        self.process = None

    def start(self, token):
        sys.path = [""]
        self.process = subprocess.Popen(
            [sys.executable, "main.py", "--token", token],
        )

    def is_running(self):
        return self.process and self.process.poll() is None

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None

class ConsoleLauncher:
    def __init__(self):
        self.launcher_process = LauncherProcess()
        self.auth_api = ApiConnector()

    def welcome(self):
        print("Welcome to Open Toontown-BR!")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")

        response = self.auth_api.authorize(username, password)
        if not response["success"]:
            print("Authentication failed.")
            return

        token = response.get("token")
        if not token:
            print("Authentication failed.")
            return
        self.launcher_process.start(token)
        self.monitor_game_process()

    def signup(self):
        email = input("Email: ")
        username = input("New Username: ")
        password = input("New Password: ")

        response = self.auth_api.signup(email, username, password)
        if not response["success"]:
            print("Signup failed.")
            return

        print("Signup successful!")

    def monitor_game_process(self):
        """Monitors if the game has closed to recreate the launcher window"""
        while self.launcher_process.is_running():
            time.sleep(1)  # Check every 1 second

        print("The game has closed.")
        self.main_menu()

    def main_menu(self):
        self.welcome()
        while True:
            print("\n1. Login")
            print("2. Signup")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.login()
            elif choice == "2":
                self.signup()
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    launcher = ConsoleLauncher()
    launcher.main_menu()