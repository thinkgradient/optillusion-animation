import requests
import os
import io
import csv
import tqdm
from PIL import Image
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

phi_step = 1
image_path = "/home/byteb/duckorrabbit.png"
output_path = "rotated_images"

COMPUTERVISION_LOCATION = os.environ.get("COMPUTERVISION_LOCATION", "westeurope")

IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")

subscription_key = "azure_computer_vision_subscription_key"

def image_analysis_in_stream(subscription_key):
    """ImageAnalysisInStream.
    This will analyze an image from a stream and return all available features.
    """
    client = ComputerVisionClient(
        endpoint="https://" + COMPUTERVISION_LOCATION + ".api.cognitive.microsoft.com/",
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    with open(os.path.join(IMAGES_FOLDER, "duckorrabbit.png"), "rb") as image_stream:
        image_analysis = client.analyze_image_in_stream(
            image=image_stream,
            visual_features=[
                VisualFeatureTypes.image_type, # Could use simple str "ImageType"
                VisualFeatureTypes.faces,      # Could use simple str "Faces"
                VisualFeatureTypes.categories, # Could use simple str "Categories"
                VisualFeatureTypes.color,      # Could use simple str "Color"
                VisualFeatureTypes.tags,       # Could use simple str "Tags"
                VisualFeatureTypes.description # Could use simple str "Description"
            ]
        )

    print("This image can be described as: {}\n".format(image_analysis.description.captions[0].text))

    print("Tags associated with this image:\nTag\t\tConfidence")
    for tag in image_analysis.tags:
        print("{}\t\t{}".format(tag.name, tag.confidence))

    print("\nThe primary colors of this image are: {}".format(image_analysis.color.dominant_colors))

def get_rotated_image_labels(client, image, bg, phi):

    # https://stackoverflow.com/a/5253554
    rot = image.rotate(-phi)   # clockwise
    image_tf = Image.composite(rot, bg, rot)

    filename = str(phi) + '.png'
    image_tf.convert('RGB').save(os.path.join(output_path, filename))

    # https://stackoverflow.com/a/33117447
    imgByteArr = io.BytesIO()
    image_tf.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue() 

    

    with open(os.path.join(IMAGES_FOLDER, os.path.join(output_path, filename)), "rb") as image_stream:
        image_analysis = client.analyze_image_in_stream(
            image=image_stream,
            visual_features=[
                VisualFeatureTypes.image_type, # Could use simple str "ImageType"
                VisualFeatureTypes.faces,      # Could use simple str "Faces"
                VisualFeatureTypes.categories, # Could use simple str "Categories"
                VisualFeatureTypes.color,      # Could use simple str "Color"
                VisualFeatureTypes.tags,       # Could use simple str "Tags"
                VisualFeatureTypes.description # Could use simple str "Description"
            ]
        )
    
    return image_analysis


image = Image.open(image_path).convert('RGBA')
bg = Image.new('RGBA', image.size, (255,) * 4)

if __name__ == "__main__":
    t = tqdm.tqdm(range(0, 360, phi_step))
    client = ComputerVisionClient(
        endpoint="https://" + COMPUTERVISION_LOCATION + ".api.cognitive.microsoft.com/",
        credentials=CognitiveServicesCredentials(subscription_key)
    )
    with open('image_rot_results.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['phi', 'label', 'score'])
        for phi in t:
            r = get_rotated_image_labels(client, image, bg, phi)
            for tag in r.tags:
                w.writerow([phi, tag.name, tag.confidence])
    