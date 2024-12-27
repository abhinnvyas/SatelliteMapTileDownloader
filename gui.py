import os
import math
import requests
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time

# Tile Calculation Functions


def get_x_tile(lon, zoom):
    return math.floor(((lon + 180) / 360) * math.pow(2, zoom))


def get_y_tile(lat, zoom):
    return math.floor((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * math.pow(2, zoom))


class TileDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Map Tile Downloader")
        self.geometry("300x300")
        self.resizable(False, False)  # Fixed window size

        # Set default values
        self.start_zoom = 0
        self.end_zoom = 0
        self.start_latitude = 0
        self.start_longitude = 0
        self.end_latitude = 0
        self.end_longitude = 0
        self.folder = "./tiles"

        # Create widgets
        self.create_widgets()

        # Variable to track download status
        self.is_downloading = False

    def create_widgets(self):
        # Create the input fields and labels in the required order
        tk.Label(self, text="Start Zoom:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w")
        self.start_zoom_entry = tk.Entry(self, width=20)
        self.start_zoom_entry.insert(0, str(self.start_zoom))
        self.start_zoom_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="End Zoom:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w")
        self.end_zoom_entry = tk.Entry(self, width=20)
        self.end_zoom_entry.insert(0, str(self.end_zoom))
        self.end_zoom_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Start Latitude:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w")
        self.start_latitude_entry = tk.Entry(self, width=20)
        self.start_latitude_entry.insert(0, str(self.start_latitude))
        self.start_latitude_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Start Longitude:").grid(
            row=3, column=0, padx=5, pady=5, sticky="w")
        self.start_longitude_entry = tk.Entry(self, width=20)
        self.start_longitude_entry.insert(0, str(self.start_longitude))
        self.start_longitude_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="End Latitude:").grid(
            row=4, column=0, padx=5, pady=5, sticky="w")
        self.end_latitude_entry = tk.Entry(self, width=20)
        self.end_latitude_entry.insert(0, str(self.end_latitude))
        self.end_latitude_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="End Longitude:").grid(
            row=5, column=0, padx=5, pady=5, sticky="w")
        self.end_longitude_entry = tk.Entry(self, width=20)
        self.end_longitude_entry.insert(0, str(self.end_longitude))
        self.end_longitude_entry.grid(row=5, column=1, padx=5, pady=5)

        # Folder selection with browse button
        tk.Label(self, text="Save Folder:").grid(
            row=6, column=0, padx=5, pady=5, sticky="w")
        self.folder_entry = tk.Entry(self, width=20)
        self.folder_entry.insert(0, self.folder)
        self.folder_entry.grid(row=6, column=1, padx=5, pady=5)

        # Browse button
        self.browse_button = tk.Button(
            self, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=6, column=2, padx=5, pady=5)

        # Status label above the button
        self.status_label = tk.Label(
            self, text="Start Downloading Now...", fg="green", font=("Helvetica", 8))
        self.status_label.grid(
            row=7, column=0, columnspan=2, padx=5, pady=5, sticky="n")

        # Start/Stop button centered below the status label
        self.download_button = tk.Button(
            self, text="Start Download", width=20, command=self.toggle_download, bg="green", fg="white")
        self.download_button.grid(
            row=8, column=0, columnspan=2, padx=5, pady=10)

    def browse_folder(self):
        # Open a directory chooser dialog
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_entry.delete(0, tk.END)  # Clear current folder entry
            # Set the new folder path
            self.folder_entry.insert(0, folder_selected)

    def toggle_download(self):
        if self.is_downloading:
            self.stop_download()
        else:
            self.start_download()

    def start_download(self):
        # Get input values
        try:
            self.start_zoom = int(self.start_zoom_entry.get())
            self.end_zoom = int(self.end_zoom_entry.get())
            self.start_latitude = float(self.start_latitude_entry.get())
            self.start_longitude = float(self.start_longitude_entry.get())
            self.end_latitude = float(self.end_latitude_entry.get())
            self.end_longitude = float(self.end_longitude_entry.get())
            self.folder = self.folder_entry.get()

            # Validate folder
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

            # Disable input fields and start button
            self.disable_inputs()

            # Change button to stop
            self.download_button.config(
                text="Stop Download", bg="red", fg="white")

            # Update status
            self.status_label.config(text="Downloading tiles...", fg="orange")

            # Start the download in a separate thread
            self.is_downloading = True
            threading.Thread(target=self.download_tiles, daemon=True).start()

        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter valid numbers for latitude, longitude, and zoom levels.")

    def stop_download(self):
        self.is_downloading = False
        self.download_button.config(
            text="Start Download", bg="green", fg="white")
        self.status_label.config(text="Download Stopped", fg="red")
        self.enable_inputs()

    def disable_inputs(self):
        self.start_zoom_entry.config(state="disabled")
        self.end_zoom_entry.config(state="disabled")
        self.start_latitude_entry.config(state="disabled")
        self.start_longitude_entry.config(state="disabled")
        self.end_latitude_entry.config(state="disabled")
        self.end_longitude_entry.config(state="disabled")
        self.folder_entry.config(state="disabled")

    def enable_inputs(self):
        self.start_zoom_entry.config(state="normal")
        self.end_zoom_entry.config(state="normal")
        self.start_latitude_entry.config(state="normal")
        self.start_longitude_entry.config(state="normal")
        self.end_latitude_entry.config(state="normal")
        self.end_longitude_entry.config(state="normal")
        self.folder_entry.config(state="normal")

    def download_tiles(self):
        # Iterate over zoom levels
        for z in range(self.start_zoom, self.end_zoom + 1):
            if not self.is_downloading:
                break

            z_folder = os.path.join(self.folder, str(z))
            os.makedirs(z_folder, exist_ok=True)

            start_x = get_x_tile(self.start_longitude, z)
            end_x = get_x_tile(self.end_longitude, z)
            start_y = get_y_tile(self.start_latitude, z)
            end_y = get_y_tile(self.end_latitude, z)

            # Download tiles for each x, y coordinate
            for x in range(start_x, end_x + 1):
                for y in range(start_y, end_y + 1):
                    if not self.is_downloading:
                        break

                    # Prepare the tile URL
                    tile_url = f"https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}"

                    # Create the subfolder for the x coordinate if not exists
                    x_folder = os.path.join(z_folder, str(x))
                    os.makedirs(x_folder, exist_ok=True)

                    # Define the file path in the format zoom/x/y.jpg
                    y_file = os.path.join(x_folder, f"{y}.jpg")

                    # Update status with the current download URL
                    self.status_label.config(
                        text=f"Downloading files for zoom level {z}: {x}, {y}", fg="orange")
                    self.update_idletasks()

                    # Download and save the tile
                    response = requests.get(tile_url)
                    if response.status_code == 200:
                        with open(y_file, 'wb') as file:
                            file.write(response.content)

            time.sleep(2)

        if self.is_downloading:
            messagebox.showinfo("Download Complete",
                                "All tiles have been downloaded.")
            self.status_label.config(text="Download Complete", fg="green")
        else:
            messagebox.showinfo("Download Stopped",
                                "Tile download has been stopped.")
            self.status_label.config(text="Download Stopped", fg="red")

        self.stop_download()


# Run the application
if __name__ == "__main__":
    app = TileDownloaderApp()
    app.mainloop()
