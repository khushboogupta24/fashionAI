from transformers import pipeline
from PIL import Image

# Initialize the object detection pipeline
pipe = pipeline("object-detection", model="valentinafeve/yolos-fashionpedia")

# List of image paths
image_paths = ["dancingqueen.jpeg", "lovelylady.jpeg", "cat.jpeg"]

# Process each image
for image_path in image_paths:
    image = Image.open(image_path)

    # Get predictions for the current image
    predictions = pipe(image)

    print(f"Predictions for image: {image_path}")
    for prediction in predictions:
        print(f"Label: {prediction['label']}")
    print()  # Add an empty line for readability between images
