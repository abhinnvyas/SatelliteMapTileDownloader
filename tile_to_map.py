import os
from PIL import Image

# Configuration
tile_size = 256  # Tile dimensions in pixels
output_folder = "./maps"  # Folder to save the combined maps
tiles_folder = "./tiles"  # Folder where tiles are stored


def stitch_tiles(zoom_level, start_x, end_x, start_y, end_y):
    """Stitch tiles for a given zoom level into a single map."""
    # Calculate the dimensions of the combined map
    width = (end_x - start_x + 1) * tile_size
    height = (end_y - start_y + 1) * tile_size
    combined_map = Image.new("RGB", (width, height))

    # Iterate through tiles and paste them into the combined map
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            tile_path = os.path.join(tiles_folder, str(
                zoom_level), str(x), f"{y}.jpg")
            if os.path.exists(tile_path):
                tile = Image.open(tile_path)
                pos_x = (x - start_x) * tile_size
                pos_y = (y - start_y) * tile_size
                combined_map.paste(tile, (pos_x, pos_y))
            else:
                print(f"Missing tile: Zoom {zoom_level}, X {x}, Y {y}")

    # Save the combined map
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"zoom_{zoom_level}.jpg")
    combined_map.save(output_path)
    print(f"Combined map saved to {output_path}")


def main():
    # Get all zoom levels from the tiles folder
    zoom_levels = [int(folder)
                   for folder in os.listdir(tiles_folder) if folder.isdigit()]
    zoom_levels.sort()

    for zoom_level in zoom_levels:
        zoom_folder = os.path.join(tiles_folder, str(zoom_level))
        if not os.path.isdir(zoom_folder):
            continue

        # Find the range of X and Y tiles
        x_tiles = [int(x) for x in os.listdir(zoom_folder) if x.isdigit()]
        x_tiles.sort()
        start_x = min(x_tiles)
        end_x = max(x_tiles)

        # Assume all X folders have the same Y range
        y_tiles = []
        for x in x_tiles:
            y_folder = os.path.join(zoom_folder, str(x))
            if os.path.isdir(y_folder):
                y_tiles.extend([int(y.split(".")[0])
                               for y in os.listdir(y_folder) if y.endswith(".jpg")])
        y_tiles.sort()
        start_y = min(y_tiles)
        end_y = max(y_tiles)

        print(
            f"Processing Zoom {zoom_level}: X [{start_x}, {end_x}], Y [{start_y}, {end_y}]")

        # Stitch tiles for this zoom level
        stitch_tiles(zoom_level, start_x, end_x, start_y, end_y)


if __name__ == "__main__":
    main()
