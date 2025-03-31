from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from image_processing import process_image

class PlateRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('车牌识别系统')
        self.setGeometry(100, 100, 800, 600)

        # 主界面布局
        self.init_ui()

    def init_ui(self):
        # 显示图片的标签
        self.image_label = QLabel('请上传一张图片', self)
        self.image_label.setGeometry(50, 50, 700, 400)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setAlignment(Qt.AlignCenter)

        # 上传按钮
        self.upload_button = QPushButton('上传图片', self)
        self.upload_button.setGeometry(150, 500, 120, 40)
        self.upload_button.clicked.connect(self.upload_image)

        # 结果显示标签
        self.result_label = QLabel('识别结果：', self)
        self.result_label.setGeometry(300, 500, 450, 40)
        self.result_label.setStyleSheet("border: 1px solid gray;")
        self.result_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Images (*.png *.jpg *.jpeg)')
        if not file_path:
            return

        # 显示上传的图片
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))
        self.result_label.setText('识别结果：处理中...')

        try:
            # 调用处理函数
            processed_image, ocr_results = process_image(file_path)
            self.display_results(ocr_results)
        except Exception as e:
            self.result_label.setText(f'识别结果：处理图片出错 ({str(e)})')

    def display_results(self, results):
        try:
            # 提取实际内容
            if not results or not isinstance(results, list):
                self.result_label.setText('识别结果：无效的结果')
                return

            # 解包多层嵌套
            extracted = results[0][0] if isinstance(results[0], list) and len(results[0]) > 0 else None
            if not extracted or len(extracted) < 2:
                self.result_label.setText('识别结果：无效的结果')
                return

            coordinates = extracted[0]  # 坐标列表
            plate_text, confidence = extracted[1]  # 车牌号和置信度

            # 格式化输出
            coords_str = ', '.join([f"({x:.1f}, {y:.1f})" for x, y in coordinates])
            text = f"车牌号：{plate_text} | 置信度：{confidence:.2%} "
            self.result_label.setText(f'识别结果：{text}')
        except Exception as e:
            print(f"display_results 出错: {e}")
            self.result_label.setText('识别结果：错误')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlateRecognitionApp()
    window.show()
    sys.exit(app.exec_())
