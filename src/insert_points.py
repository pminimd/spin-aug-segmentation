import json
import math

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def insert_points(points, max_dist=20):
    new_points = []
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        new_points.append(p1)
        dist = distance(p1, p2)
        if dist > max_dist:
            num_insert_points = int(dist // max_dist)
            for j in range(1, num_insert_points + 1):
                new_point = [
                    p1[0] + j * (p2[0] - p1[0]) / (num_insert_points + 1),
                    p1[1] + j * (p2[1] - p1[1]) / (num_insert_points + 1)
                ]
                new_points.append(new_point)
    new_points.append(points[-1])  # 添加最后一个点
    return new_points

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 写入 JSON 文件
def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# 处理 shapes 数据
def process_shapes(json_data):
    for shape in json_data.get("shapes", []):
        shape["points"] = insert_points(shape["points"])
    return json_data

if __name__ == "__main__":
    input_file = "a.json"  # 输入 JSON 文件
    output_file = "a_processed.json"  # 输出 JSON 文件
    
    data = load_json(input_file)
    processed_data = process_shapes(data)
    save_json(processed_data, output_file)
    
    print(f"处理完成，结果已保存至 {output_file}")
