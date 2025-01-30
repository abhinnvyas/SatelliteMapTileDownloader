"# SatelliteMapTileDownloader"

## Overview

SatelliteMapTileDownloader is a tool designed to download satellite map tiles from various map providers. It allows users to specify the area of interest and download the corresponding map tiles for offline use.

## Features

- Download satellite map tiles from multiple providers
- Specify area of interest using coordinates
- Save tiles for offline use

## Installation

To install the SatelliteMapTileDownloader, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/SatelliteMapTileDownloader.git
cd SatelliteMapTileDownloader
pip install -r requirements.txt
```

## Usage

To use the SatelliteMapTileDownloader, run the following command:

```bash
python main.py
```

Add all the required values and the tiles will get downloaded in the ./tiles folder.

To Stitch the downloaded tiles together for each zoom level run the following command:

```bash
python tile_to_map.py
```

By default this script assumes that the tiles are stored in the ./tiles folder.
