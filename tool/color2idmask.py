import os
from PIL import Image
import numpy as np
from .mapping import color2id_mapping

def color2idmask(colorpng_path: str, outputpng_path: str):
    
    img = Image.open(colorpng_path).convert('RGB')
    img_data = np.array(img)

    # 创建空数组保存类别索引
    class_mask = np.zeros((img_data.shape[0], img_data.shape[1]), dtype=np.uint8)

    # 将每个像素的 RGB 值映射为对应索引
    for rgb, idx in color2id_mapping.items():
        mask = np.all(img_data == rgb, axis=-1)
        class_mask[mask] = idx

    # 保存为 L 模式灰度图
    mask_img = Image.fromarray(class_mask, mode='L')
    mask_img.save(outputpng_path)

    print(f"转换完成: {outputpng_path}")

if __name__ == "__main__":
    colorpng_path = "./2008_001810_color.png"
    idmaskpng_path = "./2008_001810_idmask.png"
    color2idmask(colorpng_path, idmaskpng_path)