"""
Color analysis utilities for image processing
"""

import os
import json
import numpy as np
from PIL import Image


def analyze_histogram(image, input_path, output_path=None):
    """Analyze and optionally save image histogram"""
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Calculate histogram for each channel
    hist_r = image.histogram()[0:256]
    hist_g = image.histogram()[256:512]
    hist_b = image.histogram()[512:768]

    histogram_data = {
        "red_channel": hist_r,
        "green_channel": hist_g,
        "blue_channel": hist_b,
        "total_pixels": image.width * image.height,
    }

    print(f"Image: {os.path.basename(input_path)}")
    print(f"Dimensions: {image.width}x{image.height}")
    print(f"Total pixels: {histogram_data['total_pixels']}")

    # Basic statistics
    avg_r = sum(i * hist_r[i] for i in range(256)) / sum(hist_r)
    avg_g = sum(i * hist_g[i] for i in range(256)) / sum(hist_g)
    avg_b = sum(i * hist_b[i] for i in range(256)) / sum(hist_b)

    print(f"Average RGB values: R={avg_r:.1f}, G={avg_g:.1f}, B={avg_b:.1f}")

    if output_path:
        with open(output_path, "w") as f:
            json.dump(histogram_data, f, indent=2)
        print(f"Histogram data saved to: {output_path}")

    return histogram_data


def extract_color_palette(image, input_path, num_colors=5):
    """Extract dominant colors from image"""
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize image for faster processing
    image_resized = image.resize((150, 150))

    # Convert to numpy array and reshape
    img_array = np.array(image_resized)
    pixels = img_array.reshape(-1, 3)

    # Use k-means clustering to find dominant colors
    try:
        from sklearn.cluster import KMeans

        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)

        print(f"Dominant colors in {os.path.basename(input_path)}:")
        for i, color in enumerate(colors, 1):
            hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
            print(f"  {i}. RGB({color[0]}, {color[1]}, {color[2]}) - {hex_color}")

        return colors.tolist()
    except ImportError:
        print("scikit-learn not installed. Using simple color extraction...")
        # Fallback to simple method
        unique_colors = {}
        for pixel in pixels:
            color = tuple(pixel)
            unique_colors[color] = unique_colors.get(color, 0) + 1

        # Get most common colors
        sorted_colors = sorted(unique_colors.items(), key=lambda x: x[1], reverse=True)
        top_colors = [list(color[0]) for color in sorted_colors[:num_colors]]

        print(f"Most common colors in {os.path.basename(input_path)}:")
        for i, color in enumerate(top_colors, 1):
            hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
            print(f"  {i}. RGB({color[0]}, {color[1]}, {color[2]}) - {hex_color}")

        return top_colors


def split_channels(image, input_path, output_dir):
    """Split image into separate color channels"""
    if image.mode != "RGB":
        image = image.convert("RGB")

    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    base_name = Path(input_path).stem

    # Split channels
    r, g, b = image.split()

    # Save each channel
    r_path = output_path / f"{base_name}_red.png"
    g_path = output_path / f"{base_name}_green.png"
    b_path = output_path / f"{base_name}_blue.png"

    # Convert to RGB for saving (grayscale channels)
    r_img = Image.merge(
        "RGB", [r, Image.new("L", image.size, 0), Image.new("L", image.size, 0)]
    )
    g_img = Image.merge(
        "RGB", [Image.new("L", image.size, 0), g, Image.new("L", image.size, 0)]
    )
    b_img = Image.merge(
        "RGB", [Image.new("L", image.size, 0), Image.new("L", image.size, 0), b]
    )

    # Save using the same quality settings as the main class
    def save_channel(img, path):
        os.makedirs(
            os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True
        )
        img.save(path, quality=95, optimize=True)

    save_channel(r_img, str(r_path))
    save_channel(g_img, str(g_path))
    save_channel(b_img, str(b_path))

    print(f"Split channels saved to {output_dir}")
    return [str(r_path), str(g_path), str(b_path)]
