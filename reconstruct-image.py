from PIL import Image
from pathlib import Path
import numpy as np

# Load scrambled image
img = Image.open("jigsaw.webp").convert("RGB")

# Grid size
GRID = 5

# Get tile dimensions
width, height = img.size
tile_w = width // GRID
tile_h = height // GRID

# Mapping:
# (scrambled_row, scrambled_col) -> (original_row, original_col)
mapping = {
    (0, 0): (2, 1),
    (0, 1): (1, 1),
    (0, 2): (4, 1),
    (0, 3): (0, 3),
    (0, 4): (0, 1),

    (1, 0): (1, 4),
    (1, 1): (2, 0),
    (1, 2): (2, 4),
    (1, 3): (4, 2),
    (1, 4): (2, 2),

    (2, 0): (0, 0),
    (2, 1): (3, 2),
    (2, 2): (4, 3),
    (2, 3): (3, 0),
    (2, 4): (3, 4),

    (3, 0): (1, 0),
    (3, 1): (2, 3),
    (3, 2): (3, 3),
    (3, 3): (4, 4),
    (3, 4): (0, 2),

    (4, 0): (3, 1),
    (4, 1): (1, 2),
    (4, 2): (1, 3),
    (4, 3): (0, 4),
    (4, 4): (4, 0),
}

# Create empty reconstructed image
reconstructed = Image.new("RGB", (width, height))

# Reassemble image
for (sr, sc), (orow, ocol) in mapping.items():

    # Crop tile from scrambled image
    left = sc * tile_w
    upper = sr * tile_h
    right = left + tile_w
    lower = upper + tile_h

    tile = img.crop((left, upper, right, lower))

    # Paste into correct position
    dest_x = ocol * tile_w
    dest_y = orow * tile_h

    reconstructed.paste(tile, (dest_x, dest_y))

# Convert to numpy array with high precision
arr = np.array(reconstructed).astype(np.float64)

# Extract RGB channels
r = arr[:, :, 0]
g = arr[:, :, 1]
b = arr[:, :, 2]

# Luminance grayscale conversion using round-half-up to match forensic expectations
lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
# Round half up: add 0.5 then floor (works for non-negative values)
gray = np.clip(np.floor(lum + 0.5), 0, 255).astype(np.uint8)

# Create grayscale image and save losslessly
gray_img = Image.fromarray(gray, mode="L")
gray_img.save("reconstructed_grayscale.png", format="PNG")

print("Saved reconstructed_grayscale.png")