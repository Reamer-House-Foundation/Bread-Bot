from flask import Flask, request

# Takes awhile to import these.. do it after we have verified the user's parameters
from transformers import (
    ViTForImageClassification,
    ViTFeatureExtractor,
    ViTImageProcessor,
)

from torchvision.transforms import (
    CenterCrop,
    Compose,
    Normalize,
    RandomHorizontalFlip,
    RandomResizedCrop,
    Resize,
    ToTensor,
)

import torch

from PIL import Image

MODEL_PATH = 'outputs/'

# Load in the model for the bread bot
model = ViTForImageClassification.from_pretrained(MODEL_PATH, local_files_only=True)

model_name_or_path: str = 'google/vit-base-patch16-224-in21k'
cache_dir: str = None
model_revision: str = 'main'
use_auth_token: bool = False

image_processor = ViTImageProcessor.from_pretrained(
    model_name_or_path,
    cache_dir=cache_dir,
    revision=model_revision,
    use_auth_token=use_auth_token,
)

# Define torchvision transforms to be applied to each image.
if "shortest_edge" in image_processor.size:
    size = image_processor.size["shortest_edge"]
else:
    size = (image_processor.size["height"], image_processor.size["width"])

normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)

_test_transforms = Compose(
    [
        Resize(size),
        CenterCrop(size),
        ToTensor(),
        normalize,
    ]
)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image data from the request
    file = request.files['image']

    # Do something with the image data (e.g. save it to disk, process it, etc.)
    file.save('tmp_bread.jpg')

    image = Image.open('tmp_bread.jpg')

    processed = image_processor(image)
    processed.pixel_values = _test_transforms(image.convert('RGB'))
    outputs = model(torch.reshape(processed.pixel_values, (1, 3, 224, 224)))

    # obtain the class
    logits = outputs.logits

    prediction = logits.argmax(-1)
    return f'> Predicted class: {model.config.id2label[prediction.item()]}\n'

@app.route('/')
def hello():
	return "Hello World!"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
