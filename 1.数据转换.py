import os
from PIL import Image

# 映射表
provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂",
             "湘",
             "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U',
       'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']


def convert_to_yolo_format(file_name, image_folder, output_folder):
    # 解析文件名
    parts = file_name.split('-')
    # 01 - 90_78 - 181 & 326_369 & 395 - 375 & 403_178 & 391_165 & 323_362 & 335 - 0_0_23_25_33_30_9 - 94 - 13.jpg
    if len(parts) < 5:          #如果标签长度不足，添加空标签  # 如果没有车牌
        label_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.txt')
        with open(label_file, 'w') as f:
            # 创建空标签文件
            pass
        print(f"Processed: {file_name}, No license plate")
        return  # 跳过这个图像


    # 车牌框坐标 (第三部分: 左上 & 右下)
    box_coords = parts[2].split('&')  # 按 '&' 分割
    box_coords = [coord.split('_') for coord in box_coords]  # 对每个部分再按 '_' 分割
    box_coords = [item for sublist in box_coords for item in sublist]      #将结果展平
    x1, y1 = int(box_coords[0]), int(box_coords[1])
    x2, y2 = int(box_coords[2]), int(box_coords[3])


    # 提取图像路径，获取图像大小
    image_path = os.path.join(image_folder, file_name)
    with Image.open(image_path) as img:
        width, height = img.size

    # 计算归一化的边界框
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    box_width = x2 - x1
    box_height = y2 - y1

    # 归一化坐标
    x_center_normalized = x_center / width
    y_center_normalized = y_center / height
    box_width_normalized = box_width / width
    box_height_normalized = box_height / height

    # 车牌号码 (第五部分)
    license_plate = parts[4].split('_')
    province_code = int(license_plate[0])
    plate_chars = [ads[int(license_plate[i])] for i in range(1, 7)]
    full_plate = provinces[province_code] + ''.join(plate_chars)

    # YOLO 格式输出
    label_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.txt')
    with open(label_file, 'w') as f:
        # 假设车牌为唯一目标，所以类 ID 为 0
        class_id = 0
        f.write(
            f"{class_id} {x_center_normalized} {y_center_normalized} {box_width_normalized} {box_height_normalized}\n")

    print(f"Processed: {file_name}, Plate: {full_plate}")


def convert_ccpd_to_yolo(image_folder, output_folder):
    # 遍历 CCPD 数据集中的所有文件
    for file_name in os.listdir(image_folder):
        if file_name.endswith('.jpg'):  # 只处理图片文件
            convert_to_yolo_format(file_name, image_folder, output_folder)

if __name__ == "__main__":
    image_folder = 'E:/studycode/py/12/yolo and paddleOCR/datasets/images'
    output_folder = 'E:/studycode/py/12/yolo and paddleOCR/datasets/labels'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    convert_ccpd_to_yolo(image_folder, output_folder)
    print("所有文件已处理完成！")
