from transformers import pipeline
from PIL import Image

# Initialize the object detection pipeline
pipe = pipeline("object-detection", model="valentinafeve/yolos-fashionpedia")

# List of image paths
image_paths = ["group.jpeg", "dancingqueen.jpeg", "lovelylady.jpeg", "cat.jpeg", "backless.jpeg", "beach.jpeg"]

# Dictionary to store label occurrences
label_counts = {}

# Process each image
for image_path in image_paths:
    image = Image.open(image_path)

    # Get predictions for the current image
    predictions = pipe(image)

    print(f"Predictions for image: {image_path}")
    for prediction in predictions:
        print(f"Label: {prediction['label']}")
    print()

#jump the second shoe

    # Update label counts
    for prediction in predictions:
        label = prediction['label']
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1


# Find the label with the maximum occurrence
max_label = max(label_counts, key=label_counts.get)
max_occurrence = label_counts[max_label]

print(f"The most common label is '{max_label}' with {max_occurrence} occurrences.")
