import os
import math
import requests

# Configuration
start_zoom = 15
end_zoom = 19

start_latitude = 13.06637
start_longitude = 80.23895

end_latitude = 13.05991
end_longitude = 80.24551

folder = "./tiles"  # Folder to save the tiles

# URL for satellite image tiles
url = "https://mt0.google.com/vt/lyrs=s&hl=en&x={x_value}&y={y_value}&z={z_value}"


def get_x_tile(lon, zoom):
    return math.floor(((lon + 180) / 360) * math.pow(2, zoom))


def get_y_tile(lat, zoom):
    return math.floor((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * math.pow(2, zoom))


# Iterate over zoom levels
for z in range(start_zoom, end_zoom + 1):
    z_folder = os.path.join(folder, str(z))
    os.makedirs(z_folder, exist_ok=True)

    start_x = get_x_tile(start_longitude, z)
    end_x = get_x_tile(end_longitude, z)
    start_y = get_y_tile(start_latitude, z)
    end_y = get_y_tile(end_latitude, z)

    print(f"Start X: {start_x}, End X: {end_x}")
    print(f"Start Y: {start_y}, End Y: {end_y}")

    # Download tiles for each x, y coordinate
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            x_folder = os.path.join(z_folder, str(x))
            os.makedirs(x_folder, exist_ok=True)
            y_file = os.path.join(x_folder, f"{y}.jpg")

            # Prepare the tile URL
            tile_url = url.format(x_value=x, y_value=y, z_value=z)
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
