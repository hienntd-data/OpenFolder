import os
import customtkinter as ctk
from tkinter import messagebox
import subprocess

def get_latest_folder(parent_folder):
    try:
        subfolders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, d))]
        if not subfolders:
            return None
        latest_folder = max(subfolders, key=os.path.getmtime)
        return latest_folder
    except Exception as e:
        return None

def open_latest_folder(folder_name):
    parent_path = os.path.join(record_path, folder_name)
    if os.path.exists(parent_path):
        latest_folder = get_latest_folder(parent_path)
        if latest_folder and os.path.exists(latest_folder):
            os.startfile(latest_folder)
        else:
            messagebox.showerror("Error", f"Could not find the latest subfolder in '{folder_name}'!")
    else:
        messagebox.showerror("Error", f"Folder '{folder_name}' does not exist!")

# Mark as online-only to free up space in OneDrive folder
def free_up_space():
    try:
        for root_dir, dirs, files in os.walk(record_path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                subprocess.run(["attrib", "+U", file_path], shell=True)  
        messagebox.showinfo("Success", "Freed up space in Record folder by making files online-only!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not free up space: {e}")

def open_bat_file():
    if os.path.exists(bat_file_path):
        subprocess.run(["cmd", "/c", bat_file_path], shell=True)
    else:
        messagebox.showerror("Error", "Batch file not found!")

if __name__ == "__main__":
    folder_path = r""
    bat_file_path = r""  
    
    # Create GUI window
    ctk.set_appearance_mode("Dark")  # Use dark mode
    ctk.set_default_color_theme("dark-blue")
    
    root = ctk.CTk()
    root.title("Open Folder")
    
    # Automatically adjust window size based on content
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    # Folder list with button labels
    folder_buttons = {"A": "Name of A", "B": "Name of B", "Others": "Others", "C": "Name of C", "Free Up Space": "Free Up Space", "Run Batch File": "Run Batch File"}
    button_commands = {"Name of A": lambda: open_latest_folder("A"), "Name of B": lambda: open_latest_folder("B"), "Others": lambda: open_latest_folder("Others"), "Name of C": lambda: open_latest_folder("C"), "Free Up Space": free_up_space, "Run Batch File": open_bat_file}
    
    # Create a frame for the button layout
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, padx=20, pady=20)
    
    # Arrange buttons in a 3x2 grid
    row, col = 0, 0
    for button_name, command in button_commands.items():
        btn = ctk.CTkButton(frame, text=button_name, command=command, width=150, height=40)
        btn.grid(row=row, column=col, padx=10, pady=10)
        col += 1
        if col > 1:  # Switch to next row after 2 columns
            col = 0
            row += 1
    
    # Update window size to fit content
    root.update_idletasks()
    window_width = frame.winfo_reqwidth() + 40
    window_height = frame.winfo_reqheight() + 40
    root.geometry(f"{window_width}x{window_height}")
    root.mainloop()
