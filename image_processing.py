import os
from PIL import Image
import torch
import cv2
from paddleocr import PaddleOCR, draw_ocr

def process_image(image_path):
    #加载YOLO模型
    global cropped_path, line, ocr_result
    model = torch.hub.load('ultralytics/yolov5', 'custom',
                           path='E:/studycode/py/12/yolo and paddleOCR/1/yolov5-master/runs/train/exp3/weights/best.pt')

    # 初始化OCR模型，使用中文识别模型
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 可根据需要选择其他语言

    # 配置模型参数
    model.conf = 0.25  # 置信度阈值
    model.iou = 0.45  # IoU 阈值

    # 定义输出文件夹
    output_folder = r'runs/detect/images'
    cropped_folder = r'runs/detect/cropped'

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(cropped_folder, exist_ok=True)

    file_name = os.path.basename(image_path)

    # 加载图片
    img = Image.open(image_path)
    file_name = os.path.basename(image_path)

    # 进行检测
    results = model(img)

    # 保存检测结果
    results.save(save_dir=output_folder, exist_ok=True)  # 保存结果到同一文件夹
    #     print(f"检测完成：{file_name}")
    # except Exception as e:
    #     print(f"无法处理文件 {file_name}: {e}")
    # 获取检测到的结果
    detections = results.pandas().xyxy[0]  # 获取边界框信息
    img_cv2 = cv2.imread(image_path)

    ocr_results = []

    # 遍历所有检测到的目标并裁剪
    for idx, row in detections.iterrows():
        # 获取边界框坐标
        x_min, y_min, x_max, y_max = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])

        # 裁剪图片
        cropped_img = img_cv2[y_min:y_max, x_min:x_max]

        # 保存裁剪的图片
        cropped_file_name = f"{os.path.splitext(file_name)[0]}_crop_{idx + 1}.jpg"
        cropped_path = os.path.join(cropped_folder, cropped_file_name)
        cv2.imwrite(cropped_path, cropped_img)

        # OCR识别
        ocr_result = ocr.ocr(cropped_img, cls=True)
        ocr_results.append(ocr_result)

        # 输出识别结果
        for line in ocr_result[0]:
            print(f"识别到的文字: {line[1][0]} (置信度: {line[1][1]})")

    print(f"检测完成：{os.path.basename(image_path)}")  # 只打印文件名

    # coordinates = results[0][0][0]
    # plate_data = results[0][0][1]
    # return coordinates, plate_data

    return img,ocr_result



