import os
import math
import requests
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class TileDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Tile Downloader")

        # Variables
        self.folder_var = tk.StringVar(value="./tiles")
        self.start_zoom_var = tk.IntVar()
        self.end_zoom_var = tk.IntVar()
        self.start_lat_var = tk.DoubleVar()
        self.start_lon_var = tk.DoubleVar()
        self.end_lat_var = tk.DoubleVar()
        self.end_lon_var = tk.DoubleVar()

        self.downloading = False
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()
        self.pause_event.set()  # Initially set to allow running

        # GUI Setup
        self.setup_gui()

    def setup_gui(self):
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack()

        # Input fields
        tk.Label(input_frame, text="Start Zoom:").grid(
            row=0, column=0, sticky="e")
        tk.Entry(input_frame, textvariable=self.start_zoom_var).grid(
            row=0, column=1)

        tk.Label(input_frame, text="End Zoom:").grid(
            row=1, column=0, sticky="e")
        tk.Entry(input_frame, textvariable=self.end_zoom_var).grid(
            row=1, column=1)

        tk.Label(input_frame, text="Start Latitude:").grid(
            row=2, column=0, sticky="e")
        tk.Entry(input_frame, textvariable=self.start_lat_var).grid(
            row=2, column=1)

        tk.Label(input_frame, text="Start Longitude:").grid(
            row=3, column=0, sticky="e")
        tk.Entry(input_frame, textvariable=self.start_lon_var).grid(
            row=3, column=1)

        tk.Label(input_frame, text="End Latitude:").grid(
            row=4, column=0, sticky="e")
        tk.Entry(input_frame, textvariable=self.end_lat_var).grid(
            row=4, column=1)

        tk.Label(input_frame, text="End Longitude:").grid(
            row=5, column=0, sticky="e")
        tk.Entry(input_frame, textvariable=self.end_lon_var).grid(
            row=5, column=1)

        tk.Label(input_frame, text="Save Folder:").grid(
            row=6, column=0, sticky="e")
        tk.Entry(input_frame, textvariable=self.folder_var).grid(
            row=6, column=1)
        tk.Button(input_frame, text="Browse",
                  command=self.browse_folder).grid(row=6, column=2)

        # Progress bar and status
        self.progress_bar = ttk.Progressbar(
            self.root, length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.status_label = tk.Label(
            self.root, text="Ready to download tiles.", anchor="w")
        self.status_label.pack(pady=10)

        # Control buttons
        self.control_frame = tk.Frame(self.root, pady=10)
        self.control_frame.pack()

        self.start_pause_button = tk.Button(
            self.control_frame, text="Start Download", command=self.start_pause_download)
        self.start_pause_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(
            self.control_frame, text="Stop Download", state="disabled", command=self.stop_download)
        self.stop_button.pack(side="left", padx=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_var.set(folder_selected)

    def start_pause_download(self):
        if not self.downloading:  # Start download
            self.downloading = True
            self.start_pause_button.config(text="Pause Download")
            self.stop_button.config(state="normal")
            self.stop_event.clear()
            self.pause_event.set()  # Ensure the thread is allowed to run

            self.download_thread = threading.Thread(
                target=self.download_tiles)
            self.download_thread.start()
        elif self.pause_event.is_set():  # Pause download
            self.pause_event.clear()
            self.start_pause_button.config(text="Resume Download")
        else:  # Resume download
            self.pause_event.set()
            self.start_pause_button.config(text="Pause Download")

    def stop_download(self):
        self.stop_event.set()
        self.pause_event.set()  # Unblock if paused
        self.downloading = False
        self.start_pause_button.config(text="Start Download")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Download stopped.")

    def download_tiles(self):
        for z in range(self.start_zoom_var.get(), self.end_zoom_var.get() + 1):
            z_folder = os.path.join(self.folder_var.get(), str(z))
            os.makedirs(z_folder, exist_ok=True)

            start_x = get_x_tile(self.start_lon_var.get(), z)
            end_x = get_x_tile(self.end_lon_var.get(), z)
            start_y = get_y_tile(self.start_lat_var.get(), z)
            end_y = get_y_tile(self.end_lat_var.get(), z)

            print(f"Start X: {start_x}, End X: {end_x}")
            print(f"Start Y: {start_y}, End Y: {end_y}")

            # Download tiles for each x, y coordinate
            for x in range(start_x, end_x + 1):
                for y in range(start_y, end_y + 1):
                    x_folder = os.path.join(z_folder, str(x))
                    os.makedirs(x_folder, exist_ok=True)
                    y_file = os.path.join(x_folder, f"{y}.jpg")

                    # Prepare the tile URL
                    tile_url = "https://mt0.google.com/vt/lyrs=s&hl=en&x={x_value}&y={y_value}&z={z_value}".format(
                        x_value=x, y_value=y, z_value=z)
                    print(f"Downloading tile: {tile_url}")

                    # Download and save the tile
                    response = requests.get(tile_url)
                    if response.status_code == 200:
                        with open(y_file, 'wb') as file:
                            file.write(response.content)
                    else:
                        print(f"Failed to download tile {x}, {y} at zoom {z}")
            print(
                f"Finished downloading tiles for zoom level {z}. Sleeping for 2 seconds.")
            # Sleep for 2 seconds (to avoid hitting rate limits)
            import time
            time.sleep(2)


def get_x_tile(lon, zoom):
    return math.floor(((lon + 180) / 360) * math.pow(2, zoom))


def get_y_tile(lat, zoom):
    return math.floor((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * math.pow(2, zoom))


if __name__ == "__main__":
    root = tk.Tk()
    app = TileDownloaderApp(root)
    root.mainloop()
