# 定义颜色映射 (RGB -> 类别索引)
color2id_mapping = {
    (0, 0, 0)     : 0,             # 类别0: 黑色    "background"
    (112, 173, 71): 1              # 类别1: 青柠绿   "eagle"
}

# label和color映射放这里
label2color_mapping = {
    "background" : [0, 0, 0],      # 类别0: 黑色    "background"
    "eagle"      : [112, 173, 71], # 类别1: 青柠绿   "eagle"
}