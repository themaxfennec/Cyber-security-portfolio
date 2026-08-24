import tkinter as tk

def log_key(event):
    with open("keystrokes.txt", "a", encoding="utf-8") as f:
        f.write(f"{event.keysym}\n")

root = tk.Tk()
root.title("Keystroke Logger Demo")
root.geometry("400x200")

label = tk.Label(root, text="Type here — keystrokes are logged while this window is active.")
label.pack(pady=50)

root.bind("<KeyPress>", log_key)
root.mainloop()