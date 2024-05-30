import tkinter as tk
from keylogger import Keylogger

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Keylogger")
        self.keylogger = Keylogger()

    def start_keylogger(self):
        self.keylogger.start_keylogger()

    def stop_keylogger(self):
        self.keylogger.save_to_file()
        self.root.destroy()

    def create_gui(self):
        # Create GUI label
        label = tk.Label(self.root, text="Keylogger is running. Press Esc to stop.")
        label.pack()

        # Create GUI buttons
        start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger)
        start_button.pack()

        stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger)
        stop_button.pack()

        # Run GUI
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.create_gui()
