import os
import cv2
from PIL import Image
import json
import numpy as np
from .mapping import label2color_mapping

def json2color(json_path: str, colorpng_path: str):
    with open(json_path) as f:
        data = json.load(f)
    mask = np.zeros((data['imageHeight'], data['imageWidth'], 3), dtype=np.uint8)       
    for shape in data['shapes']:
        label = shape['label']
        points = np.array(shape['points'], dtype=np.int32)  
        color = label2color_mapping.get(label, (0, 0, 0))  #
        cv2.fillPoly(mask, [points], color) 
    mask_image = Image.fromarray(mask)
    mask_image.save(colorpng_path)

if __name__ == "__main__":
    jsonpath = "example_data/2008_001810.json"
    colorpng_path = "./2008_001810_color.png"
    json2color(jsonpath, colorpng_path)