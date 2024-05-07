import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
from collections import Counter
from transformers import pipeline

# Initialize the object detection pipeline
pipe = pipeline("object-detection", model="valentinafeve/yolos-fashionpedia")


# Function to extract top colors from an image
def extract_top_colors(image, exclude_colors, num_colors=5, threshold=50):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixels = rgb_image.reshape((-1, 3))

    filtered_pixels = [pixel for pixel in pixels if
                       all(np.linalg.norm(pixel - color) > threshold for color in exclude_colors)]

    color_counts = Counter(tuple(pixel) for pixel in filtered_pixels)

    top_colors = color_counts.most_common(num_colors)

    return [np.array(color[0]) for color in top_colors]


# Function to convert RGB color to hex format
# Function to convert RGB color to hex format
def rgb_to_hex(rgb_color):
    # Ensure rgb_color is a 1-dimensional array with 3 elements (R, G, B)
    if len(rgb_color) != 3:
        print("Warning: Invalid RGB color input. Expected 3 elements (R, G, B), but got:", rgb_color)
        return '#000000'  # Return a default color (e.g., black) or handle it as you see fit

    # Proceed with conversion if the input is valid
    return '#{:02x}{:02x}{:02x}'.format(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))



# Function to process images and return top 5 options for colors, silhouettes, and accessories
def process_images(folder_path, exclude_colors, num_colors=5):
    all_color_counts = Counter()
    silhouettes_label_counts = Counter()  # Counter for silhouettes
    accessories_label_counts = Counter()  # Counter for accessories

    # Define categories for silhouettes and accessories
    silhouettes = [
        'shirt, blouse', 'top, t-shirt, sweatshirt', 'sweater', 'cardigan',
        'jacket', 'vest', 'pants', 'shorts', 'skirt', 'coat', 'dress', 'jumpsuit',
        'cape', 'hood', 'collar', 'lapel', 'sleeve', 'pocket'
    ]
    accessories = [
        'glasses', 'hat', 'headband, head covering, hair accessory', 'tie',
        'glove', 'watch', 'belt', 'bag, wallet', 'scarf', 'umbrella', 'leg warmer',
        'tights, stockings', 'sock', 'shoe', 'neckline', 'buckle', 'zipper',
        'applique', 'bead', 'bow', 'flower', 'fringe', 'ribbon', 'rivet', 'ruffle',
        'sequin', 'tassel', 'epaulette'
    ]

    # Process each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = Image.open(file_path)

            # Run predictions on the image
            predictions = pipe(image)

            print(f"Predictions for image: {file_name}")

            # Categorize labels as silhouettes or accessories and update counters
            for prediction in predictions:
                label = prediction['label']
                print(f"Label: {label}")

                if label in silhouettes:
                    silhouettes_label_counts[label] += 1
                elif label in accessories:
                    accessories_label_counts[label] += 1

            # Process colors and update color counter
            img_cv2 = cv2.imread(file_path)
            top_colors = extract_top_colors(img_cv2, exclude_colors, num_colors=num_colors)

            all_color_counts.update(map(tuple, top_colors))

    # Get top 5 overall colors
    sorted_colors = all_color_counts.most_common(num_colors)
    top_colors_list = [rgb_to_hex(np.array(color)) for color, count in sorted_colors]

    # Get top 5 silhouettes labels
    top_silhouettes_labels = silhouettes_label_counts.most_common(5)
    top_silhouettes_list = [label for label, count in top_silhouettes_labels]

    # Get top 5 accessories labels
    top_accessories_labels = accessories_label_counts.most_common(5)
    top_accessories_list = [label for label, count in top_accessories_labels]

    # Return the top 5 options for colors, silhouettes, and accessories
    return top_colors_list, top_silhouettes_list, top_accessories_list, folder_path


# Function to display images based on user selection
def display_images(top_colors, top_silhouettes, top_accessories, folder_path):
    selected_color = colors_combobox.get()
    selected_silhouette = silhouettes_combobox.get()
    selected_accessory = accessories_combobox.get()

    # Filter images based on user selection
    matching_images = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = Image.open(file_path)
            predictions = pipe(image)

            # Check if the image matches the user's selections
            for prediction in predictions:
                label = prediction['label']

                if ((selected_color == 'Choose a color' or
                     any(rgb_to_hex(np.array(color[0])) == selected_color for color in
                         extract_top_colors(cv2.imread(file_path), [], num_colors=5))) and
                        (selected_silhouette == 'Choose a silhouette' or label == selected_silhouette) and
                        (selected_accessory == 'Choose an accessory' or label == selected_accessory)):
                    matching_images.append((file_path, image))
                    break

    # Display the matching images in a new window
    display_window = tk.Toplevel()
    display_window.title("Matching Images")

    # Display each matching image in the new window
    for file_path, image in matching_images:
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(display_window, image=img)
        img_label.image = img  # Keep a reference to the image
        img_label.pack(pady=5)


# Function to create the GUI
def create_gui(folder_path, grass_colors):
    global colors_combobox, silhouettes_combobox, accessories_combobox

    # Create a window
    root = tk.Tk()
    root.title("Top 5 Options")

    # Process the images and get top 5 options
    top_colors, top_silhouettes, top_accessories, folder_path = process_images(folder_path, grass_colors)

    # Create dropdown menu for top 5 overall colors
    colors_label = ttk.Label(root, text="Select a color:")
    colors_label.pack(pady=5)

    colors_combobox = ttk.Combobox(root, values=top_colors)
    colors_combobox.set("Choose a color")
    colors_combobox.pack(pady=5)

    # Create dropdown menu for top 5 silhouettes
    silhouettes_label = ttk.Label(root, text="Select a silhouette:")
    silhouettes_label.pack(pady=5)

    silhouettes_combobox = ttk.Combobox(root, values=top_silhouettes)
    silhouettes_combobox.set("Choose a silhouette")
    silhouettes_combobox.pack(pady=5)

    # Create dropdown menu for top 5 accessories
    accessories_label = ttk.Label(root, text="Select an accessory:")
    accessories_label.pack(pady=5)

    accessories_combobox = ttk.Combobox(root, values=top_accessories)
    accessories_combobox.set("Choose an accessory")
    accessories_combobox.pack(pady=5)

    # Add a button to display matching images
    display_button = ttk.Button(root, text="Display Images",
                                command=lambda: display_images(top_colors, top_silhouettes, top_accessories,
                                                               folder_path))
    display_button.pack(pady=10)

    # Start the GUI
    root.mainloop()


# Folder path input and grass colors definition
folder_path = input("Enter the folder path: ")

grass_colors = [
    np.array([99, 103, 67]),
    np.array([133, 146, 85]),
    np.array([63, 66, 39]),
    np.array([174, 183, 118]),
    np.array([232, 217, 179])
]


# Create the GUI
create_gui(folder_path, grass_colors)
