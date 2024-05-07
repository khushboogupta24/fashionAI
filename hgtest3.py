# Use a pipeline as a high-level helper
#from transformers import pipeline
from PIL import Image

from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained("Falah/fashion-model")

image_path = "examplepics/dancingqueen.jpeg"
image = Image.open(image_path)

predictions = pipe(image)

for prediction in predictions:
    print(f"Label: {prediction['label']}, Score: {prediction['score']}, Box: {prediction['box']}")
