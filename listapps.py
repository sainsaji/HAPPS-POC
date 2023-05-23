import json
import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def install_happs(happs_entry):
    happs_name = happs_entry["happs-name"]
    happs_icon = happs_entry["happs-icon"]
    happs_version = happs_entry["happs-version"]
    happs_directory = happs_entry["happs-directory"]

    # Create the 'happs-installed' folder if it doesn't exist
    os.makedirs("happs-installed", exist_ok=True)

    # Copy the files for the selected .happs entry to the 'happs-installed' folder
    dest_directory = os.path.join("happs-installed", happs_name)
    os.makedirs(dest_directory, exist_ok=True)
    shutil.copy2(happs_directory, dest_directory)
    shutil.copy2(happs_icon, dest_directory)

    messagebox.showinfo("Install", f"{happs_name} installed successfully!")

def view_happs_config():
    # Load the configuration data from the file
    with open(file_path, "r") as f:
        config_data = json.load(f)

    # Extract the "happs-config" entries
    happs_entries = config_data["happs-config"]

    # Create the main window
    root = tk.Tk()
    root.title("Happs Config Viewer")

    # Define the grid parameters
    num_columns = 3
    grid_padding = 20

    # Iterate over the happs entries
    for i, entry in enumerate(happs_entries):
        happs_name = entry["happs-name"]
        happs_icon = entry["happs-icon"]
        happs_version = entry["happs-version"]

        # Load the icon image and resize it
        icon_image = Image.open(happs_icon)
        icon_size = (100, 100)  # Adjust the size as per your requirement
        icon_image = icon_image.resize(icon_size, Image.LANCZOS)

        # Convert the image to Tkinter format
        tk_icon_image = ImageTk.PhotoImage(icon_image)

        # Create a frame for each app entry
        frame = tk.Frame(root, padx=grid_padding, pady=grid_padding)
        frame.grid(row=i // num_columns, column=i % num_columns)

        # Create a label for the app icon
        icon_label = tk.Label(frame, image=tk_icon_image)
        icon_label.image = tk_icon_image  # Save a reference to avoid garbage collection
        icon_label.pack()

        # Create a label for the app name
        name_label = tk.Label(frame, text=happs_name, font=("Helvetica", 12))
        name_label.pack()

        # Create a label for the app version
        version_label = tk.Label(frame, text=happs_version, font=("Helvetica", 10))
        version_label.pack()

        # Create an install button
        install_button = tk.Button(frame, text="Install \U0001F680", command=lambda entry=entry: install_happs(entry))
        install_button.pack()

    root.mainloop()

# Define the file path
file_path = "conf.json"

# Check if the file exists
if not os.path.exists(file_path):
    messagebox.showerror("Error", "Configuration file not found!")
else:
    view_happs_config()
