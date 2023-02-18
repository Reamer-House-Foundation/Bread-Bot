import os
import sys

if len(sys.argv) < 2:
    print('Give me a path to an image.')
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print(f'{sys.argv[1]} is not a path to an image.')
    sys.exit(1)

# Takes awhile to import these.. do it after we have verified the user's parameters
from transformers import (
    ViTForImageClassification,
    ViTFeatureExtractor
)

from PIL import Image

MODEL_PATH = 'outputs/'

# Load in the model for the bread bot
model = ViTForImageClassification.from_pretrained(MODEL_PATH, local_files_only=True)

image = Image.open(sys.argv[1])

feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
encoding = feature_extractor(images=image, return_tensors='pt')
encoding.keys()
pixel_values = encoding['pixel_values']

outputs = model(pixel_values)
logits = outputs.logits

prediction = logits.argmax(-1)
print('>>>>>>>>>>')
print(f'> Predicted class: {model.config.id2label[prediction.item()]}')
print('>>>>>>>>>>')
