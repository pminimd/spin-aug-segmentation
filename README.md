# SpinAugSegmentation: 支持**旋转任意角度**的分割标注增强

可以对以 JSON 文件存储的 COCO 格式分割标注进行**旋转增强**

增强前：
![alt text](assest/before_aug.png)

增强后：
![alt text](assest/after_aug.png)

使用样例见pipeline.py

1. 环境安装：
```bash
pip install -r requirements.txt
```
2. 在pipeline.py中的第7行设置原始数据集目录：
```python
# 混合存放原图和原始标注的文件夹
example_datadir = "./example_data"
```
3. 在函数 augment_image_and_annotation 中设置数据增强的参数，若不设置则采用默认值
```python
augment_image_and_annotation(imagefilepath, 
                             labelfilepath, 
                             i, 
                             angles=180, 
                             crop_scale=[0.8, 0.99],
                             target_size=(513, 513))
```
4. 运行
```bash
python pipeline.py
```
