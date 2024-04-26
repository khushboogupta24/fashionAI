from transformers import pipeline
from PIL import Image
import os

# Initialize the object detection pipeline
pipe = pipeline("object-detection", model="valentinafeve/yolos-fashionpedia")

# Prompt the user to enter a folder name
folder_path = input("Enter the folder name: ")

# Dictionary to store label occurrences
label_counts = {}

# Process each image in the folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    # Check if the file is an image
    if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        image = Image.open(file_path)

        # Get predictions for the current image
        predictions = pipe(image)

        print(f"Predictions for image: {file_name}")
        # Print predictions for each image
        for prediction in predictions:
            print(f"Label: {prediction['label']}")
        print()

        # Update label counts
        for prediction in predictions:
            label = prediction['label']
            if label in label_counts:
                label_counts[label] += 1
            else:
                label_counts[label] = 1

# Sort label counts by occurrences in descending order
sorted_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)

# Print the top 5 labels
print("Top 5 labels:")
for label, count in sorted_labels[:5]:
    print(f"Label: {label}, Occurrences: {count}")
