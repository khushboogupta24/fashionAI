import cv2
import numpy as np
from sklearn.cluster import KMeans

def extract_colors(image_path, num_colors=5):
    print("Image path:", image_path)
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Unable to load the image. Please check the file path and file integrity.")
        return None

    resized_image = cv2.resize(image, (300, 300))

    pixels = resized_image.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_

    return colors.astype(int)

image_path = '/Users/xiomara/Desktop/sd/dancingqueen.jpeg'
colors = extract_colors(image_path)
if colors is not None:
    print("Dominant Colors (RGB format):")
    for color in colors:
        print(color)
