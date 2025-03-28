import os
from src.spin_aug import augment_image_and_annotation
from tool.json2color import json2color
from tool.color2idmask import color2idmask


# 你混合存放原图和原始标注的文件夹
example_datadir = "./example_data"

# 将origin数据集增强后，image保存在aug_images/, json保存在aug_jsons/
for filename in os.listdir(example_datadir):
    
    if not filename.endswith(".jpg"):
         continue
    else:
        if os.path.exists(os.path.join(example_datadir, filename.replace('.jpg', '.json'))):
            print(f"Warning: Image {filename} missing annotation file")
    
    imagefilepath = os.path.join(example_datadir, filename)
    labelfilepath = os.path.join(example_datadir, filename.replace('.jpg', '.json'))

    # 重复以生成10张增强图
    for i in range(10):
        augment_image_and_annotation(imagefilepath, labelfilepath, i, angles=180, crop_scale=[0.8, 0.99], target_size=(513, 513))

# 将增强后的aug_jsons/ 批量生成 aug_colormasks/
for json_file in os.listdir("aug_jsons/"):
    json_path = os.path.join("aug_jsons/", json_file)
    json2color(json_path, os.path.join("aug_colormasks/", json_file.replace('.json', '.png')))

# 将aug_colormasks/ 批量生成 aug_idmasks/
for colorpng_file in os.listdir("aug_colormasks/"):
    colorpng_path = os.path.join("aug_colormasks/", colorpng_file)
    color2idmask(colorpng_path, os.path.join("aug_idmasks/", colorpng_file))