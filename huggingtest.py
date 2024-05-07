# Use a pipeline as a high-level helper
from transformers import pipeline
from PIL import Image

pipe = pipeline("object-detection", model="valentinafeve/yolos-fashionpedia")

# image_path = "dancingqueen.jpeg"
# image = Image.open(image_path)
#
image_path = "examplepics/watch.jpg"
image = Image.open(image_path)

# image_path = "cat.jpeg"
# image = Image.open(image_path)

predictions = pipe(image)

for prediction in predictions:
    print(f"Label: {prediction['label']}")

#for prediction in predictions:
    #print(f"Label: {prediction['label']}, Score: {prediction['score']}, Box: {prediction['box']}")
