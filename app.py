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

def open_other_folders():
    try:
        excluded_folders = {"A", "B", "C"}
        all_folders = [d for d in os.listdir(record_path) if os.path.isdir(os.path.join(record_path, d)) and d not in excluded_folders]
        
        if not all_folders:
            messagebox.showinfo("Info", "No other folders found!")
            return
        
        for folder in all_folders:
            os.startfile(os.path.join(record_path, folder))
    except Exception as e:
        messagebox.showerror("Error", f"Could not open other folders: {e}")

def free_up_space():
    try:
        for root_dir, dirs, files in os.walk(record_path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                subprocess.run(["attrib", "+U", file_path], shell=True)  # Mark as online-only
        messagebox.showinfo("Success", "Freed up space in Record folder by making files online-only!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not free up space: {e}")

def open_bat_file():
    if os.path.exists(bat_file_path):
        subprocess.run(["cmd", "/c", bat_file_path], shell=True)
    else:
        messagebox.showerror("Error", "Batch file not found!")

if __name__ == "__main__":
    record_path = r""
    bat_file_path = r""
    
    ctk.set_appearance_mode("Dark")  # Use dark mode
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Open Folder")
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    folder_buttons = {"A": "A", "B": "B", "Others": "Others", "C": "C", "Free Up Space": "Free Up Space", "Run Batch File": "Run Batch File"}
    button_commands = {"A": lambda: open_latest_folder("A"), "B": lambda: open_latest_folder("B"), "Others": open_other_folders, "C": lambda: open_latest_folder("C"), "Free Up Space": free_up_space, "Run Batch File": open_bat_file}
    
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, padx=20, pady=20)
    
    row, col = 0, 0
    for button_name, command in button_commands.items():
        btn = ctk.CTkButton(frame, text=button_name, command=command, width=150, height=40)
        btn.grid(row=row, column=col, padx=10, pady=10)
        col += 1
        if col > 1:
            col = 0
            row += 1
    
    root.update_idletasks()
    window_width = frame.winfo_reqwidth() + 40
    window_height = frame.winfo_reqheight() + 40
    root.geometry(f"{window_width}x{window_height}")
    root.mainloop()
