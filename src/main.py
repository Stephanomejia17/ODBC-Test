import tkinter as tk
from gui.app_window import FabricacionApp

def main():
    root = tk.Tk()
    app = FabricacionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()