import os
import math
import requests
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

# Function to calculate tile coordinates


def get_x_tile(lon, zoom):
    return math.floor(((lon + 180) / 360) * math.pow(2, zoom))


def get_y_tile(lat, zoom):
    return math.floor((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * math.pow(2, zoom))

# Download and display the tiles


def download_tiles(start_zoom, end_zoom, start_latitude, start_longitude, end_latitude, end_longitude, folder, canvas, status_label):
    url = "https://mt0.google.com/vt/lyrs=s&hl=en&x={x_value}&y={y_value}&z={z_value}"

    # Tile size (in pixels)
    tile_size = 256

    # Iterate over zoom levels
    for z in range(start_zoom, end_zoom + 1):
        z_folder = os.path.join(folder, str(z))
        os.makedirs(z_folder, exist_ok=True)

        start_x = get_x_tile(start_longitude, z)
        end_x = get_x_tile(end_longitude, z)
        start_y = get_y_tile(start_latitude, z)
        end_y = get_y_tile(end_latitude, z)

        print(f"Downloading tiles at zoom level {z}...")

        total_tiles = (end_x - start_x + 1) * (end_y - start_y + 1)
        downloaded_tiles = 0

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                x_folder = os.path.join(z_folder, str(x))
                os.makedirs(x_folder, exist_ok=True)
                y_file = os.path.join(x_folder, f"{y}.jpg")

                # Prepare the tile URL
                tile_url = url.format(x_value=x, y_value=y, z_value=z)

                # Download the tile
                response = requests.get(tile_url)
                if response.status_code == 200:
                    with open(y_file, 'wb') as file:
                        file.write(response.content)

                    # Load the image and display it on the canvas
                    img = Image.open(y_file)
                    img = img.resize((tile_size, tile_size),
                                     Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)

                    # Calculate the position for this tile on the canvas
                    pos_x = (x - start_x) * tile_size
                    pos_y = (y - start_y) * tile_size

                    # Place the image on the canvas
                    canvas.create_image(pos_x, pos_y, image=img_tk)
                    canvas.image = img_tk  # Keep a reference

                    downloaded_tiles += 1
                    status_label.config(
                        text=f"Downloading tiles... {downloaded_tiles}/{total_tiles} tiles downloaded")
                    canvas.update_idletasks()
                else:
                    print(f"Failed to download tile {x}, {y} at zoom {z}")

        print(
            f"Finished downloading tiles for zoom level {z}. Sleeping for 2 seconds.")
        time.sleep(2)

    # Final message once download is complete
    messagebox.showinfo("Download Complete", "All tiles have been downloaded!")

# GUI for input fields and real-time status


def start_download():
    try:
        start_zoom = int(start_zoom_entry.get())
        end_zoom = int(end_zoom_entry.get())
        start_latitude = float(start_latitude_entry.get())
        start_longitude = float(start_longitude_entry.get())
        end_latitude = float(end_latitude_entry.get())
        end_longitude = float(end_longitude_entry.get())

        folder = "./tiles"  # Folder to save the tiles

        # Initialize canvas for map tiles
        canvas.delete("all")  # Clear the canvas before drawing new tiles

        # Start a thread for downloading tiles
        download_thread = threading.Thread(target=download_tiles, args=(
            start_zoom, end_zoom, start_latitude, start_longitude, end_latitude, end_longitude, folder, canvas, status_label))
        download_thread.start()

    except ValueError:
        messagebox.showerror(
            "Input Error", "Please enter valid numeric values.")


# GUI setup using Tkinter
root = tk.Tk()
root.title("Tile Downloader and Viewer")

# Input fields for start and end zoom, latitudes, and longitudes
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Start Zoom:").grid(row=0, column=0)
start_zoom_entry = tk.Entry(frame)
start_zoom_entry.grid(row=0, column=1)

tk.Label(frame, text="End Zoom:").grid(row=1, column=0)
end_zoom_entry = tk.Entry(frame)
end_zoom_entry.grid(row=1, column=1)

tk.Label(frame, text="Start Latitude:").grid(row=2, column=0)
start_latitude_entry = tk.Entry(frame)
start_latitude_entry.grid(row=2, column=1)

tk.Label(frame, text="Start Longitude:").grid(row=3, column=0)
start_longitude_entry = tk.Entry(frame)
start_longitude_entry.grid(row=3, column=1)

tk.Label(frame, text="End Latitude:").grid(row=4, column=0)
end_latitude_entry = tk.Entry(frame)
end_latitude_entry.grid(row=4, column=1)

tk.Label(frame, text="End Longitude:").grid(row=5, column=0)
end_longitude_entry = tk.Entry(frame)
end_longitude_entry.grid(row=5, column=1)

# Button to start the tile download
start_button = tk.Button(root, text="Start Download", command=start_download)
start_button.pack(pady=10)

# Status label to show download progress
status_label = tk.Label(root, text="Ready to download tiles.")
status_label.pack(pady=10)

# Canvas to show the downloaded map tiles
canvas = tk.Canvas(root, width=768, height=768)  # Adjust canvas size as needed
canvas.pack()

root.mainloop()
