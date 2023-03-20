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

image = Image.open(sys.argv[1])

# Scale the image

# The following is based off of a notebook I found published, but the FeatureExtractor
# class gives me a deprication warning when I import it
# https://github.com/NielsRogge/Transformers-Tutorials/blob/master/VisionTransformer/Quick_demo_of_HuggingFace_version_of_Vision_Transformer_inference.ipynb
#feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
#encoding = feature_extractor(images=image, return_tensors='pt')
#encoding.keys()
#pixel_values = encoding['pixel_values']
#outputs = model(pixel_values)

# The following was hacked together, and I'm not sure if it is scaling things properly
# for the model, but the model accepts it

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


processed = image_processor(image)
processed.pixel_values = _test_transforms(image.convert('RGB'))
outputs = model(torch.reshape(processed.pixel_values, (1, 3, 224, 224)))

# obtain the class
logits = outputs.logits

prediction = logits.argmax(-1)
print('>>>>>>>>>>')
print(f'> Predicted class: {model.config.id2label[prediction.item()]}')
print('>>>>>>>>>>')
