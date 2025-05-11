import sys
import time
import pyautogui
import numpy as np
import cv2
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QTextEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt
from screeninfo import get_monitors
from src.program import Programn

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        primary_screen = get_monitors()[0]  # Lấy thông tin màn hình chính (số 1)
        self.screen_1_bbox = (0, 0, primary_screen.width, primary_screen.height)  # Tọa độ màn hình
        print(f"Kích thước màn hình số 1: {self.screen_1_bbox}")
        self.program = Programn(region=self.screen_1_bbox)  # Khởi tạo đối tượng Programn

        self.running = True  # Trạng thái chạy của chương trình
        self.cycle_count = 0  # Số chu trình đã chạy

        self.setWindowTitle("Bot Clicker")
        self.setGeometry(100, 100, 400, 300)

        # Layout chính
        layout = QVBoxLayout()

        # Label và TextEdit cho SEARCH_QUERY
        self.search_query_label = QLabel("SEARCH_QUERY:")
        self.search_query_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.search_query_label)

        self.search_query_text = QTextEdit()
        self.search_query_text.setPlaceholderText("Nhập SEARCH_QUERY tại đây...")
        layout.addWidget(self.search_query_text)

        # Label và TextEdit cho Keywords
        self.keywords_label = QLabel("Keywords:")
        self.keywords_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.keywords_label)

        self.keywords_text = QTextEdit()
        self.keywords_text.setPlaceholderText("Nhập keywords tại đây...")
        layout.addWidget(self.keywords_text)

        # Nút Run
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_program)
        layout.addWidget(self.run_button)

        # Nút Stop
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_program)
        layout.addWidget(self.stop_button)

        # Label hiển thị số chu trình đã chạy
        self.cycle_label = QLabel("Số chu trình đã chạy: 0")
        self.cycle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.cycle_label)

        # Tạo widget chính và đặt layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_program(self):
        """
        Hàm chạy chương trình khi nhấn nút Run.
        """
        search_query = self.search_query_text.toPlainText().strip()
        keywords = self.keywords_text.toPlainText().strip()

        if not search_query or not keywords:
            print("Vui lòng nhập cả SEARCH_QUERY và keywords.")
            return

        self.running = True  # Đặt trạng thái chạy
        self.run_button.setStyleSheet("background-color: green; color: white;")  # Đổi màu nút Run sang xanh
        threading.Thread(target=self.run_bot, args=(search_query, keywords), daemon=True).start()

    def stop_program(self):
        """
        Hàm dừng chương trình khi nhấn nút Stop.
        """
        print("Đang dừng chương trình sau khi hoàn thành chu trình hiện tại...")
        self.running = False  # Đặt trạng thái dừng
        self.run_button.setStyleSheet("")  # Đặt lại màu nút Run về mặc định

    def run_bot(self, search_query, keywords):
        """
        Chạy toàn bộ chương trình.
        """
        while self.running:  # Kiểm tra trạng thái chạy
            # Đọc template icon Google
            template_image = cv2.imread(r".\assets\google_icon.JPG")
            if template_image is None:
                print("Không thể đọc template icon Google.")
                return

            # Chụp ảnh màn hình
            screenshot = pyautogui.screenshot(region=self.screen_1_bbox)
            screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Bước 1: Tìm icon Google và double click
            self.program.step_1_find_google_icon_and_double_click(template_image, screenshot_np)
            time.sleep(1)

            # Bước 2: Tìm space bar của Google và click
            screenshot = pyautogui.screenshot(region=self.screen_1_bbox)
            screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            self.program.step_2_find_google_space_bar_and_click(screenshot_np)
            time.sleep(1)

            # Bước 3: Nhập từ khóa tìm kiếm và nhấn Enter
            self.program.step_3_enter_search_keyword_and_press_enter(search_query)
            time.sleep(1)

            # Bước 4: Tìm kiếm từ khóa và click vào từ khóa
            screenshot = pyautogui.screenshot(region=self.screen_1_bbox)
            screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            self.program.step_4_find_and_click_search_result(keywords, screenshot_np)

            # Tăng số chu trình đã chạy
            self.cycle_count += 1
            self.cycle_label.setText(f"Số chu trình đã chạy: {self.cycle_count}")

            # Đợi một khoảng thời gian trước khi bắt đầu lại
            print("Hoàn thành một chu kỳ, bắt đầu lại...")
            time.sleep(1)  # Đợi 1 giây trước khi lặp lại

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())