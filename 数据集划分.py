import os
import shutil
import random


def split_dataset(image_folder, label_folder, output_folder, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    # 获取所有图像文件名
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]  # 只处理 jpg 文件

    # 打乱图像文件顺序
    random.shuffle(image_files)

    # 计算训练集、验证集、测试集的大小
    total_count = len(image_files)
    train_count = int(total_count * train_ratio)
    val_count = int(total_count * val_ratio)
    test_count = total_count - train_count - val_count  # 剩下的归为测试集

    # 分割图像文件
    train_images = image_files[:train_count]
    val_images = image_files[train_count:train_count + val_count]
    test_images = image_files[train_count + val_count:]

    # 移动图像文件和标签文件
    def move_files(image_list, data_split):
        for image_name in image_list:
            # 图像文件路径
            image_path = os.path.join(image_folder, image_name)
            label_path = os.path.join(label_folder, os.path.splitext(image_name)[0] + '.txt')

            # 目标路径
            image_dst = os.path.join(output_folder, data_split, 'images', image_name)
            label_dst = os.path.join(output_folder, data_split, 'labels', os.path.splitext(image_name)[0] + '.txt')

            # 移动图像文件和标签文件
            shutil.copy(image_path, image_dst)
            shutil.copy(label_path, label_dst)

    # 将文件分别复制到训练集、验证集和测试集目录
    move_files(train_images, 'train')
    move_files(val_images, 'val')
    move_files(test_images, 'test')

    print(f"Dataset split complete: {train_count} training, {val_count} validation, {test_count} testing")


if __name__ == "__main__":                          # 设置路径
    image_folder = 'E:/studycode/py/12/yolo and paddleOCR/datasets/images'  # 图像文件夹路径
    label_folder = 'E:/studycode/py/12/yolo and paddleOCR/datasets/labels'  # 标签文件夹路径
    output_folder = 'E:/studycode/py/12/yolo and paddleOCR/data_hf'  # 输出分割后的数据集路径

    # 调用函数
    split_dataset(image_folder, label_folder, output_folder)
    print("数据集划分完毕！")
