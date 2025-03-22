import os
import sys
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Constants
CONFIG_FILE = "config.txt"
EXCLUDED_FOLDERS = {"A", "B", "C"}

# Load and Save Config
def load_config():
    """Load paths from config.txt if it exists."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip().split("\n")
    return ["", ""]

def save_config(record_path, bat_path):
    """Save paths to config.txt."""
    if not record_path or not bat_path:
        messagebox.showwarning("Warning", "Please select both paths before saving!")
        return False

    with open(CONFIG_FILE, "w") as f:
        f.write(f"{record_path}\n{bat_path}")
    return True

# Folder Operations
def get_latest_folder(parent_folder):
    """Get the most recently modified subfolder in the parent folder."""
    if not os.path.exists(parent_folder):
        return None
    try:
        subfolders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) 
                      if os.path.isdir(os.path.join(parent_folder, d))]
        return max(subfolders, key=os.path.getmtime) if subfolders else None
    except Exception as e:
        print(f"Error getting latest folder: {e}")
        return None

def open_folder(folder_path):
    """Open a folder using the system's default file explorer."""
    if not os.path.exists(folder_path):
        return f"❌ Folder '{folder_path}' does not exist!"

    try:
        if sys.platform == "win32":
            os.startfile(folder_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", folder_path])
        else:
            subprocess.run(["xdg-open", folder_path])
        return f"✅ Opened: {folder_path}"
    except Exception as e:
        return f"❌ Error opening folder: {e}"

def open_latest_folder(record_path, folder_name, status_label):
    """Open the latest subfolder in a specific folder (A, B, or C)."""
    if not record_path:
        status_label.configure(text="❌ Record path is not set!", text_color="red")
        return

    parent_path = os.path.join(record_path, folder_name)
    latest_folder = get_latest_folder(parent_path)
    
    if latest_folder:
        status_label.configure(text=open_folder(latest_folder), text_color="green")
    else:
        status_label.configure(text=f"⚠️ No recent folder in '{folder_name}', opening root...", text_color="orange")
        open_folder(parent_path)  # Open root folder if no subfolder exists

def open_other_folders(record_path, status_label):
    """Open all folders except A, B, and C."""
    if not record_path:
        status_label.configure(text="❌ Record path is not set!", text_color="red")
        return

    try:
        base_folders = [os.path.join(record_path, d) for d in os.listdir(record_path) 
                        if os.path.isdir(os.path.join(record_path, d)) and d not in EXCLUDED_FOLDERS]
        
        if not base_folders:
            status_label.configure(text="⚠️ No other folders found!", text_color="orange")
            return

        for folder in base_folders:
            open_folder(folder)
        status_label.configure(text="✅ Opened all other folders.", text_color="green")
    except Exception as e:
        status_label.configure(text=f"❌ Error opening other folders: {e}", text_color="red")

# Utility Functions
def free_up_space(record_path, status_label):
    """Free up space by modifying file attributes (Windows only)."""
    if not record_path:
        status_label.configure(text="❌ Record path is not set!", text_color="red")
        return

    try:
        for root_dir, _, files in os.walk(record_path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                subprocess.run(["attrib", "+U", file_path], shell=True)
        status_label.configure(text="✅ Space freed up successfully!", text_color="green")
    except Exception as e:
        status_label.configure(text=f"❌ Error freeing up space: {e}", text_color="red")

def open_bat_file(bat_path, status_label):
    """Execute a batch file."""
    if not bat_path:
        status_label.configure(text="❌ Batch file path is not set!", text_color="red")
        return

    if os.path.exists(bat_path):
        subprocess.Popen(["cmd.exe", "/c", "start", "", bat_path], shell=True)
        status_label.configure(text="✅ Batch file executed successfully!", text_color="green")
    else:
        status_label.configure(text="❌ Batch file not found!", text_color="red")

# GUI Setup
def setup_gui():
    """Setup the main GUI window."""
    root = ctk.CTk()
    root.title("Folder Manager")
    root.geometry("500x500")
    root.resizable(False, False)

    # Load config
    record_path, bat_path = load_config()

    # If config is not set, show setup window
    if not record_path or not bat_path:
        setup_window(root)
    else:
        main_window(root, record_path, bat_path)

    root.mainloop()

def setup_window(root):
    """Show setup window to configure paths."""
    setup_frame = ctk.CTkFrame(root)
    setup_frame.pack(pady=20, padx=20, fill="both", expand=True)

    ctk.CTkLabel(setup_frame, text="Setup Required", font=("Arial", 16, "bold")).pack(pady=10)

    ctk.CTkLabel(setup_frame, text="Record Path:", font=("Arial", 14)).pack(pady=5)
    record_path_entry = ctk.CTkEntry(setup_frame, width=400)
    record_path_entry.pack(pady=5)
    ctk.CTkButton(setup_frame, text="📂 Browse", command=lambda: browse_record(record_path_entry)).pack(pady=5)

    ctk.CTkLabel(setup_frame, text="Batch File Path:", font=("Arial", 14)).pack(pady=5)
    bat_file_path_entry = ctk.CTkEntry(setup_frame, width=400)
    bat_file_path_entry.pack(pady=5)
    ctk.CTkButton(setup_frame, text="📄 Browse", command=lambda: browse_bat(bat_file_path_entry)).pack(pady=5)

    ctk.CTkButton(setup_frame, text="💾 Save Config", command=lambda: save_and_continue(root, record_path_entry, bat_file_path_entry)).pack(pady=10)

def browse_record(entry):
    """Browse for record folder."""
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, "end")
        entry.insert(0, folder)

def browse_bat(entry):
    """Browse for batch file."""
    file = filedialog.askopenfilename(filetypes=[("Batch Files", "*.bat")])
    if file:
        entry.delete(0, "end")
        entry.insert(0, file)

def save_and_continue(root, record_path_entry, bat_file_path_entry):
    """Save config and continue to main window."""
    record_path = record_path_entry.get().strip()
    bat_path = bat_file_path_entry.get().strip()

    if save_config(record_path, bat_path):
        # Clear setup frame and open main window
        for widget in root.winfo_children():
            widget.destroy()
        main_window(root, record_path, bat_path)

def main_window(root, record_path, bat_path):
    """Show main window with functionality."""
    # UI Elements
    ctk.CTkLabel(root, text="Folder Manager", font=("Arial", 16, "bold")).pack(pady=10)

    # Status Label
    status_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
    status_label.pack(pady=10)

    # Buttons
    buttons = [
        ("📁 Open A", lambda: open_latest_folder(record_path, "A", status_label)),
        ("📁 Open B", lambda: open_latest_folder(record_path, "B", status_label)),
        ("📁 Open C", lambda: open_latest_folder(record_path, "C", status_label)),
        ("📂 Other Folders", lambda: open_other_folders(record_path, status_label)),
        ("💾 Free Up Space", lambda: free_up_space(record_path, status_label)),
        ("⚡ Run Batch File", lambda: open_bat_file(bat_path, status_label))
    ]

    for text, command in buttons:
        ctk.CTkButton(root, text=text, width=200, height=40, command=command).pack(pady=10)

# Main Execution
if __name__ == "__main__":
    setup_gui()
