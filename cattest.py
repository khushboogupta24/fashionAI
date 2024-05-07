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
    silhouettes_label_counts = Counter()  # Counter for silhouettes
    accessories_label_counts = Counter()  # Counter for accessories

    # Define the categories
    silhouettes = [
        'shirt, blouse', 'top, t-shirt, sweatshirt', 'sweater', 'cardigan',
        'jacket', 'vest', 'pants', 'shorts', 'skirt', 'coat', 'dress', 'jumpsuit',
        'cape',  'hood', 'collar', 'lapel', 'sleeve', 'pocket'

    ]
    accessories = [
        'glasses', 'hat', 'headband, head covering, hair accessory', 'tie',
        'glove', 'watch', 'belt', 'bag, wallet', 'scarf', 'umbrella', 'leg warmer', 'tights, stockings', 'sock', 'shoe',
        'neckline', 'buckle', 'zipper', 'applique', 'bead', 'bow', 'flower', 'fringe',
        'ribbon', 'rivet', 'ruffle', 'sequin', 'tassel', 'epaulette',
    ]

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = Image.open(file_path)

            predictions = pipe(image)

            print(f"Predictions for image: {file_name}")

            for prediction in predictions:
                label = prediction['label']
                print(f"Label: {label}")

                # Categorize the label into silhouettes or accessories
                if label in silhouettes:
                    silhouettes_label_counts[label] += 1
                elif label in accessories:
                    accessories_label_counts[label] += 1

            print()

            # Process colors
            img_cv2 = cv2.imread(file_path)
            top_colors = extract_top_colors(img_cv2, exclude_colors, num_colors=num_colors)

            all_color_counts.update(map(tuple, top_colors))

    # Print top 5 overall colors
    sorted_colors = all_color_counts.most_common(num_colors)
    print("Top 5 overall colors (Hex format):")
    for color, count in sorted_colors:
        print(rgb_to_hex(np.array(color)))

    # Print top 5 silhouettes labels
    print("\nTop 5 silhouettes labels:")
    top_silhouettes_labels = silhouettes_label_counts.most_common(5)
    for label, count in top_silhouettes_labels:
        print(f"{label}: {count} times")

    # Print top 5 accessories labels
    print("\nTop 5 accessories labels:")
    top_accessories_labels = accessories_label_counts.most_common(5)
    for label, count in top_accessories_labels:
        print(f"{label}: {count} times")

# Folder path input and grass colors definition
folder_path = input("Enter the folder name: ")

grass_colors = [
    np.array([99, 103, 67]),
    np.array([133, 146, 85]),
    np.array([63, 66, 39]),
    np.array([174, 183, 118]),
    np.array([232, 217, 179])
]

# Process images and print top 5 colors and labels
process_images(folder_path, grass_colors)
