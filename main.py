import json
import os
import tkinter as tk
from tkinter import messagebox

def update_config():
    # Create a new window for updating configuration
    window = tk.Toplevel(root)
    window.title("Update Configuration")

    # Label and entry for wifi-ssid
    tk.Label(window, text="WiFi SSID:").grid(row=0, column=0, padx=10, pady=10)
    ssid_entry = tk.Entry(window)
    ssid_entry.grid(row=0, column=1)

    # Label and entry for password
    tk.Label(window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(window)
    password_entry.grid(row=1, column=1)

    def save_config():
        ssid = ssid_entry.get()
        password = password_entry.get()

        # Update the configuration data
        config_data["wifi"]["wifi-ssid"] = ssid
        config_data["wifi"]["password"] = password

        # Write the updated configuration data to the file
        with open(file_path, "w") as f:
            json.dump(config_data, f, indent=4)

        messagebox.showinfo("Configuration Updated", "Configuration updated successfully.")
        window.destroy()
        update_main_window()  # Update the main window with new changes

    # Button to save the updated configuration
    save_button = tk.Button(window, text="Save", command=save_config)
    save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def update_main_window():
    ssid_label.config(text="WiFi SSID: " + config_data["wifi"]["wifi-ssid"])
    password_label.config(text="Password: " + config_data["wifi"]["password"])

# Define the file path
file_path = "conf.json"

# Create the main window
root = tk.Tk()
root.title("Configuration")

if os.path.exists(file_path):
    # Load the existing configuration data
    with open(file_path, "r") as f:
        config_data = json.load(f)

    # Display the content of the conf.json file
    ssid_label = tk.Label(root, text="WiFi SSID: " + config_data["wifi"]["wifi-ssid"])
    ssid_label.pack(padx=10, pady=5)

    password_label = tk.Label(root, text="Password: " + config_data["wifi"]["password"])
    password_label.pack(padx=10, pady=5)

    # Button to update the configuration
    update_button = tk.Button(root, text="Update Configuration", command=update_config)
    update_button.pack(padx=10, pady=10)
else:
    # Create the conf.json file
    config_data = {
        "wifi": {
            "wifi-ssid": "testwifi",
            "password": "supersecretpassword"
        }
    }

    with open(file_path, "w") as f:
        # Write the configuration data to the file
        json.dump(config_data, f, indent=4)
        print("conf.json file created.")

    # Open the update configuration window directly
    update_config()

root.mainloop()
