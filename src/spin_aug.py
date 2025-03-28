import cv2
import numpy as np
import json
import random
import math
import os
from PIL import Image
from .insert_points import process_shapes

def rotate_point(x, y, angle, center):
    angle_rad = math.radians(angle)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    new_x = cos_angle * (x - center[0]) - sin_angle * (y - center[1]) + center[0]
    new_y = sin_angle * (x - center[0]) + cos_angle * (y - center[1]) + center[1]
    return new_x, new_y

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
    return rotated_image, center, rotation_matrix

def rotate_annotation(points, rotation_matrix, width, height):
    rotated_points = []
    for point in points:
        vec = np.array([point[0], point[1], 1]).T
        new_x, new_y = rotation_matrix @ vec
        new_x = min(max(new_x, 0), width - 1)
        new_y = min(max(new_y, 0), height - 1)
        rotated_points.append([new_x, new_y])
    return rotated_points

def crop_image(image, annotations, crop_x, crop_y, crop_w, crop_h):
    cropped_image = image[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    new_shapes = []
    for shape in annotations["shapes"]:
        new_points = [[max(0, min(p[0] - crop_x, crop_w - 1)), 
                       max(0, min(p[1] - crop_y, crop_h - 1))] 
                      for p in shape["points"]]
        shape["points"] = new_points
        new_shapes.append(shape)
    annotations["shapes"] = new_shapes
    return cropped_image, annotations

def resize_image(image, annotations, target_size=(513, 513)):
    orig_h, orig_w = image.shape[:2]
    scale_x = target_size[0] / orig_w
    scale_y = target_size[1] / orig_h
    resized_image = cv2.resize(image, target_size)
    for shape in annotations["shapes"]:
        shape["points"] = [[p[0] * scale_x, p[1] * scale_y] for p in shape["points"]]
    annotations["imageHeight"], annotations["imageWidth"] = target_size
    return resized_image, annotations

def augment_image_and_annotation(image_path, json_path, id, angles=3, crop_scale=[0.8, 0.95], target_size=(513, 513)):
    image = cv2.imread(image_path)
    with open(json_path, 'r') as f:
        annotations = json.load(f)
    
    height, width = image.shape[:2]
    angle = random.uniform(-angles, angles)
    rotated_image, center, rotation_matrix = rotate_image(image, angle)
    
    for shape in annotations["shapes"]:
        shape["points"] = rotate_annotation(shape["points"], rotation_matrix, width, height)
    
    scale_factor = random.uniform(crop_scale[0], crop_scale[1])
    crop_x = random.randint(0, int(width * (1.0 - scale_factor)))
    crop_y = random.randint(0, int(height * (1.0 - scale_factor)))
    crop_w, crop_h = int(width * scale_factor), int(height * scale_factor)
    cropped_image, annotations = crop_image(rotated_image, annotations, crop_x, crop_y, crop_w, crop_h)
    
    resized_image, annotations = resize_image(cropped_image, annotations, target_size)
    cv2.imwrite(f"./aug_images/{os.path.basename(image_path).replace('.jpg', f'_{id}.jpg')}", resized_image)
    with open(f"./aug_jsons/{os.path.basename(image_path).replace('.jpg', f'_{id}.json')}", 'w') as f:
        json.dump(annotations, f)

if __name__ == "__main__":
    image_path = 'example_data/2008_001810.jpg'
    json_path = 'example_data/2008_001810.json'
    augment_image_and_annotation(image_path, json_path, 1, angles=180)