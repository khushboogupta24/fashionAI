


import cv2
import numpy as np
from collections import Counter


def extract_top_colors(image, exclude_colors, num_colors=5, threshold=50):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixels = rgb_image.reshape((-1, 3))

    filtered_pixels = [pixel for pixel in pixels if
                       all(np.linalg.norm(pixel - color) > threshold for color in exclude_colors)]

    color_counts = Counter(tuple(pixel) for pixel in filtered_pixels)

    top_colors = color_counts.most_common(num_colors)

    return [np.array(color[0]) for color in top_colors]


image = cv2.imread('/Users/xiomara/Desktop/sd/dancingqueen.jpeg')

grass_colors = [
    np.array([99, 103, 67]),
    np.array([133, 146, 85]),
    np.array([63, 66, 39]),
    np.array([174, 183, 118]),
    np.array([232, 217, 179])
]

top_colors = extract_top_colors(image, grass_colors, num_colors=5)

print("Top 5 colors (RGB format):")
for color in top_colors:
    print(color)
