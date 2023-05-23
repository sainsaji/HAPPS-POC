import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import shutil

def update_wifi_config():
    def save_config():
        ssid = ssid_entry.get()
        password = password_entry.get()

        # Update the configuration data
        config_data["wifi"]["wifi-ssid"] = ssid
        config_data["wifi"]["password"] = password

        # Write the updated configuration data to the file
        with open(file_path, "w") as f:
            json.dump(config_data, f, indent=4)

        messagebox.showinfo("Configuration Updated", "WiFi configuration updated successfully.")

    # Create the WiFi configuration tab
    wifi_tab = ttk.Frame(tab_control)
    tab_control.add(wifi_tab, text="WiFi")
    tab_control.pack(expand=1, fill="both")

    # Label and entry for wifi-ssid
    tk.Label(wifi_tab, text="WiFi SSID:").grid(row=0, column=0, padx=10, pady=10)
    ssid_entry = tk.Entry(wifi_tab)
    ssid_entry.grid(row=0, column=1)

    # Label and entry for password
    tk.Label(wifi_tab, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(wifi_tab)
    password_entry.grid(row=1, column=1)

    # Load existing values into the entry fields
    ssid_entry.insert(0, config_data["wifi"]["wifi-ssid"])
    password_entry.insert(0, config_data["wifi"]["password"])

    # Button to save the updated WiFi configuration
    save_button = tk.Button(wifi_tab, text="Save", command=save_config)
    save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def update_happs_config():
    def browse_happs_file():
        file_path = filedialog.askopenfilename(filetypes=[("Happs Files", "*.happs")])
        happs_file_entry.delete(0, tk.END)
        happs_file_entry.insert(0, file_path)
        happs_directory_entry.delete(0, tk.END)
        happs_directory_entry.insert(0, os.path.dirname(file_path))

    def browse_happs_icon():
        file_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.png;*.jpg;*.jpeg")])
        happs_icon_entry.delete(0, tk.END)
        happs_icon_entry.insert(0, file_path)

    def add_happs_config():
        happs_name = happs_name_entry.get()
        happs_version = happs_version_entry.get()
        happs_file = happs_file_entry.get()
        happs_icon = happs_icon_entry.get()
        happs_directory = happs_directory_entry.get()

        # Create a new Happs entry
        new_happs_entry = {
            "happs-name": happs_name,
            "happs-icon": happs_icon,
            "happs-version": happs_version,
            "happs-directory": happs_directory
        }

        # Copy the .happs file to the 'happs-package' directory
        dest_happs_file = os.path.join("happs-package", os.path.basename(happs_file))
        shutil.copy2(happs_file, dest_happs_file)

        # Copy the icon file to the 'happs-package' directory
        dest_icon_file = os.path.join("happs-package", os.path.basename(happs_icon))
        shutil.copy2(happs_icon, dest_icon_file)

        # Update the 'happs-directory' and 'happs-icon' fields with the new locations
        new_happs_entry["happs-directory"] = dest_happs_file
        new_happs_entry["happs-icon"] = dest_icon_file

        # Add the new Happs entry to the configuration data
        config_data["happs-config"].append(new_happs_entry)

        # Write the updated configuration data to the file
        with open(file_path, "w") as f:
            json.dump(config_data, f, indent=4)

        messagebox.showinfo("Happs Configuration", "New Happs entry added successfully.")
        update_happs_list()

    def update_happs_list():
        # Clear the existing Happs list
        for i in happs_listbox.get_children():
            happs_listbox.delete(i)

        # Load the Happs entries from the configuration data
        for entry in config_data["happs-config"]:
            happs_name = entry["happs-name"]
            happs_icon = entry["happs-icon"]
            happs_version = entry["happs-version"]
            happs_directory = entry["happs-directory"]

            # Add the Happs entry to the listbox
            happs_listbox.insert("", tk.END, values=(happs_name, happs_icon, happs_version, happs_directory))

    # Create the Happs configuration tab
    happs_tab = ttk.Frame(tab_control)
    tab_control.add(happs_tab, text="Happs Configuration")
    tab_control.pack(expand=1, fill="both")

    # Happs List
    happs_listbox = ttk.Treeview(happs_tab, columns=("Name", "Icon", "Version", "Directory"), show="headings")
    happs_listbox.heading("Name", text="Name")
    happs_listbox.heading("Icon", text="Icon")
    happs_listbox.heading("Version", text="Version")
    happs_listbox.heading("Directory", text="Directory")
    happs_listbox.pack(padx=10, pady=10, fill="both", expand=True)

    # Scrollbar for the Happs List
    scrollbar = ttk.Scrollbar(happs_tab, orient=tk.VERTICAL, command=happs_listbox.yview)
    happs_listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Frame for adding a new Happs entry
    add_frame = ttk.LabelFrame(happs_tab, text="Add Happs Entry")
    add_frame.pack(padx=10, pady=10)

    # Entry fields for Happs details
    tk.Label(add_frame, text="Happs Name:").grid(row=0, column=0, padx=10, pady=5)
    happs_name_entry = tk.Entry(add_frame)
    happs_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_frame, text="Happs Version:").grid(row=1, column=0, padx=10, pady=5)
    happs_version_entry = tk.Entry(add_frame)
    happs_version_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_frame, text="Happs File:").grid(row=2, column=0, padx=10, pady=5)
    happs_file_entry = tk.Entry(add_frame)
    happs_file_entry.grid(row=2, column=1, padx=10, pady=5)
    browse_file_button = tk.Button(add_frame, text="Browse", command=browse_happs_file)
    browse_file_button.grid(row=2, column=2, padx=5, pady=5)

    tk.Label(add_frame, text="Happs Icon:").grid(row=3, column=0, padx=10, pady=5)
    happs_icon_entry = tk.Entry(add_frame)
    happs_icon_entry.grid(row=3, column=1, padx=10, pady=5)
    browse_icon_button = tk.Button(add_frame, text="Browse", command=browse_happs_icon)
    browse_icon_button.grid(row=3, column=2, padx=5, pady=5)

    tk.Label(add_frame, text="Happs Directory:").grid(row=4, column=0, padx=10, pady=5)
    happs_directory_entry = tk.Entry(add_frame)
    happs_directory_entry.grid(row=4, column=1, padx=10, pady=5)

    # Button to add a new Happs entry
    add_button = tk.Button(add_frame, text="Add", command=add_happs_config)
    add_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    # Update the Happs list
    update_happs_list()
    

def update_firmware_config():
    def browse_firmware_file():
        file_path = filedialog.askopenfilename(filetypes=[("Firmware Files", "*.bin")])
        firmware_file_entry.delete(0, tk.END)
        firmware_file_entry.insert(0, file_path)
        firmware_directory_entry.delete(0, tk.END)
        firmware_directory_entry.insert(0, os.path.dirname(file_path))

    def add_happs_config():
        firmware_name = firmware_name_entry.get()
        firmware_version = firmware_version_entry.get()
        firmware_file = firmware_file_entry.get()
        firmware_directory = firmware_directory_entry.get()

        # Create a new Happs entry
        new_firmware_entry = {
            "firmware-name": firmware_name,
            "firmware-version": firmware_version,
            "firmware-directory": firmware_directory
        }

        # Copy the .happs file to the 'happs-package' directory
        dest_firmware_file = os.path.join("firmware-package", os.path.basename(firmware_file))
        shutil.copy2(firmware_file, dest_firmware_file)



        # Update the 'happs-directory' with the new locations
        new_firmware_entry["firmware-directory"] = dest_firmware_file

        # Add the new Happs entry to the configuration data
        config_data["firmware-config"].append(new_firmware_entry)

        # Write the updated configuration data to the file
        with open(file_path, "w") as f:
            json.dump(config_data, f, indent=4)

        messagebox.showinfo("firmware Configuration", "New firmware entry added successfully.")
        update_firmware_list()

    def update_firmware_list():
        # Clear the existing Happs list
        for i in firmware_listbox.get_children():
            firmware_listbox.delete(i)

        # Load the Happs entries from the configuration data
        for entry in config_data["firmware-config"]:
            firmware_name = entry["firmware-name"]
            firmware_version = entry["firmware-version"]
            firmware_directory = entry["firmware-directory"]

            # Add the Happs entry to the listbox
            firmware_listbox.insert("", tk.END, values=(firmware_name, firmware_version, firmware_directory))

    # Create the Happs configuration tab
    firmware_tab = ttk.Frame(tab_control)
    tab_control.add(firmware_tab, text="firmware Configuration")
    tab_control.pack(expand=1, fill="both")

    # Happs List
    firmware_listbox = ttk.Treeview(firmware_tab, columns=("Name", "Version", "Directory"), show="headings")
    firmware_listbox.heading("Name", text="Name")
    firmware_listbox.heading("Version", text="Version")
    firmware_listbox.heading("Directory", text="Directory")
    firmware_listbox.pack(padx=10, pady=10, fill="both", expand=True)

    # Scrollbar for the Happs List
    scrollbar = ttk.Scrollbar(firmware_tab, orient=tk.VERTICAL, command=firmware_listbox.yview)
    firmware_listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Frame for adding a new Happs entry
    add_frame = ttk.LabelFrame(firmware_tab, text="Add Firmware Entry")
    add_frame.pack(padx=10, pady=10)

    # Entry fields for Happs details
    tk.Label(add_frame, text="Firmware Name:").grid(row=0, column=0, padx=10, pady=5)
    firmware_name_entry = tk.Entry(add_frame)
    firmware_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_frame, text="Firmware Version:").grid(row=1, column=0, padx=10, pady=5)
    firmware_version_entry = tk.Entry(add_frame)
    firmware_version_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_frame, text="Firmware File:").grid(row=2, column=0, padx=10, pady=5)
    firmware_file_entry = tk.Entry(add_frame)
    firmware_file_entry.grid(row=2, column=1, padx=10, pady=5)
    browse_file_button = tk.Button(add_frame, text="Browse", command=browse_firmware_file)
    browse_file_button.grid(row=2, column=2, padx=5, pady=5)

    tk.Label(add_frame, text="Firmware Directory:").grid(row=4, column=0, padx=10, pady=5)
    firmware_directory_entry = tk.Entry(add_frame)
    firmware_directory_entry.grid(row=4, column=1, padx=10, pady=5)

    # Button to add a new Happs entry
    add_button = tk.Button(add_frame, text="Add", command=add_happs_config)
    add_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    # Update the Happs list
    update_firmware_list()

# Define the file path
file_path = "conf.json"

# Check if the file exists
if os.path.exists(file_path):
    # Load the existing configuration data
    with open(file_path, "r") as f:
        config_data = json.load(f)
else:
    # Create the default configuration data
    config_data = {
        "wifi": {
            "wifi-ssid": "testwifi",
            "password": "supersecretpassword"
        },
        "happs-config": []
    }

# Create the main window
root = tk.Tk()
root.title("Configuration")
root.geometry("500x300")  # Set the initial window size
root.resizable(True, True)  # Disable window resizing

# Create tab control for different configuration tabs
tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill="both")

# Add WiFi configuration tab
update_wifi_config()

# Add Happs configuration tab
update_happs_config()

# Add Happs configuration tab
update_firmware_config()

root.mainloop()
