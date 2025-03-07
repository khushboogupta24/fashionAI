from transformers import pipeline
from PIL import Image
import os
import cv2
import numpy as np
from collections import Counter

pipe = pipeline("object-detection", model="valentinafeve/yolos-fashionpedia")


def extract_top_colors(image, exclude_colors, num_colors=5, threshold=50):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixels = rgb_image.reshape((-1, 3))

    filtered_pixels = [pixel for pixel in pixels if
                       all(np.linalg.norm(pixel - color) > threshold for color in exclude_colors)]

    color_counts = Counter(tuple(pixel) for pixel in filtered_pixels)

    top_colors = color_counts.most_common(num_colors)

    return [np.array(color[0]) for color in top_colors]


def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))


def process_images(folder_path, exclude_colors, num_colors=5):
    all_color_counts = Counter()
    label_counts = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = Image.open(file_path)


            predictions = pipe(image)

            print(f"Predictions for image: {file_name}")

            for prediction in predictions:
                print(f"Label: {prediction['label']}")

                label = prediction['label']
                if label in label_counts:
                    label_counts[label] += 1
                else:
                    label_counts[label] = 1

            print()


            img_cv2 = cv2.imread(file_path)
            top_colors = extract_top_colors(img_cv2, exclude_colors, num_colors=num_colors)

            all_color_counts.update(map(tuple, top_colors))


    sorted_colors = all_color_counts.most_common(num_colors)


    print("Top 5 overall colors (Hex format):")
    for color, count in sorted_colors:
        print(rgb_to_hex(np.array(color)))

        # Print top 5 labels
    print("\nTop 5 labels:")
    top_labels = label_counts.most_common(5)
    for label, count in top_labels:
        print(f"{label}: {count} times")


folder_path = input("Enter the folder name: ")

grass_colors = [
    np.array([99, 103, 67]),
    np.array([133, 146, 85]),
    np.array([63, 66, 39]),
    np.array([174, 183, 118]),
    np.array([232, 217, 179])
]

process_images(folder_path, grass_colors)
