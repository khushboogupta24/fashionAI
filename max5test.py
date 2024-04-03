from transformers import pipeline
from PIL import Image
from collections import Counter

# Initialize the object detection pipeline
pipe = pipeline("object-detection", model="valentinafeve/yolos-fashionpedia")

# List of image paths
image_paths = ["dancingqueen.jpeg", "lovelylady.jpeg", "cat.jpeg", "happydude.jpeg"]

# Dictionary to store label occurrences
label_counts = Counter()

# Process each image
for image_path in image_paths:
    image = Image.open(image_path)

    # Get predictions for the current image
    predictions = pipe(image)

    # Update label counts
    for prediction in predictions:
        label = prediction['label']
        label_counts[label] += 1

# Find the top 5 most common labels
top_labels = label_counts.most_common(5)

print("Top 5 most common labels:")
for label, count in top_labels:
    print(f"Label: {label}, Occurrences: {count}")
