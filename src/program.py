import time
import numpy as np
import pyautogui
import cv2
import random
from src.template_matcher import TemplateMatcher  # Giả sử TemplateMatcher đã được định nghĩa
from src.search_key_ocr import SearchKeyOCR  # Giả sử SearchKeyOCR đã được định nghĩa
from src.keyboard_controller import KeyboardController  # Giả sử KeyBoardController đã được định nghĩa
from src.mouse_controller import MouseController  # Giả sử MouseController đã được định nghĩa

class Programn (object):
    def __init__(self, num_page_max=11, region=None):
        self.num_page_max = num_page_max
        self.region=region
        self.template_matcher = TemplateMatcher()
        self.search_key_tool = SearchKeyOCR()
        self.keyboard_controller = KeyboardController()
        self.mouse_controller = MouseController()

    def step_1_find_google_icon_and_double_click(self, template_image, screenshot):
        """
        Bước 1: Tìm vị trí của icon Google và double click.
        """
        print("Bước 1: Tìm icon Google và double click...")
        icon_position = self.template_matcher.matcher(screenshot, template_image, threshold=0.5, scales=np.linspace(0.2, 5, 40))
        if icon_position:
            self.mouse_controller.move_to(icon_position[0], icon_position[1], duration=0.2)
            self.mouse_controller.double_click()
            print("Đã double click vào icon Google.")
        else:
            print("Không tìm thấy icon Google.")

    def step_2_find_google_space_bar_and_click(self, screenshot):
        """
        Bước 2: Tìm space bar của Google và click vào vị trí điều chỉnh.
        """
        print("Bước 2: Tìm space bar của Google...")
        keyword = "Search Google"
        position, bbox = self.search_key_tool.search_first_key(keyword, screenshot)
        if position:
            adjusted_x = position[0]
            adjusted_y = position[1]
            self.mouse_controller.move_to(adjusted_x, adjusted_y, duration=0.2)
            self.mouse_controller.click()
            print(f"Đã click vào vị trí điều chỉnh: ({adjusted_x}, {adjusted_y}).")
        else:
            print("Không tìm thấy space bar của Google.")

    def step_3_enter_search_keyword_and_press_enter(self, search_query):
        """
        Bước 3: Nhập từ khóa tìm kiếm và nhấn Enter.
        """
        print(f"Bước 3: Nhập từ khóa tìm kiếm '{search_query}' và nhấn Enter...")
        self.keyboard_controller.type_text(search_query)
        time.sleep(1)  # Đợi một chút trước khi nhấn Enter
        self.keyboard_controller.press_enter()
        print("Đã nhập từ khóa và nhấn Enter.")
        self.mouse_controller.move_to(200, 200, duration=0.2)  # Di chuyển chuột về góc trên bên

    def step_4_find_and_click_search_result(self, search_keyword, screenshot):
        """
        Bước 4: Tìm kiếm từ khóa và click vào từ khóa.
        Nếu không tìm thấy từ khóa, cuộn ngẫu nhiên 200-400.
        Nếu không tìm thấy từ khóa và phát hiện ký tự hết trang, tìm vị trí của nút "Next" và click.
        Nếu tìm thấy từ khóa, click vào từ khóa, đợi 5s, sau đó di chuyển đến vị trí top-right của ảnh và click.
        """
        print(f"Bước 4: Tìm kiếm từ khóa '{search_keyword}' và click vào...")
        count_page = 0
        end_page = False
        count_scroll = 0
        while not end_page and count_page < self.num_page_max:
            # Tìm kiếm từ khóa trên ảnh chụp màn hình
            position, bbox = self.search_key_tool.search_first_key(search_keyword, screenshot)
            if position:
                # Nếu tìm thấy, click vào từ khóa
                self.mouse_controller.move_to(position[0], position[1], duration=0.2)
                self.mouse_controller.click()
                print(f"Đã click vào từ khóa '{search_keyword}' tại tọa độ: {position}.")
                time.sleep(5)  # Đợi 5 giây
                break
            else:
                # Nếu không tìm thấy từ khóa, kiểm tra ký tự hết trang
                print(f"Không tìm thấy từ khóa '{search_keyword}', đang kiểm tra ký tự hết trang...")
                if count_scroll > 5:
                    for i in range(10, 1, -1):
                        end_position, _ = self.search_key_tool.search_first_key(f"G{'o'*i}gle", screenshot)
                        if end_position:
                            break
                else:
                    end_position, _ = self.search_key_tool.search_first_key(f"G{'o'*10}gle", screenshot)
                    
                if end_position:
                    print("Đã phát hiện ký tự hết trang, tìm nút 'Next'...")
                    next_position, _ = self.search_key_tool.search_largest_bbox_key("Next", screenshot)
                    if next_position:
                        self.mouse_controller.move_to(next_position[0], next_position[1], duration=0.2)
                        self.mouse_controller.click()
                        print(f"Đã click vào nút 'Next' tại tọa độ: {next_position}.")
                        time.sleep(2)  # Đợi nội dung tải lại
                        # Cập nhật ảnh chụp màn hình sau khi click "Next"
                        screenshot = pyautogui.screenshot(region=self.region)
                        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                        count_page += 1
                        count_scroll = 0
                        continue
                    else:
                        print("Không tìm thấy nút 'Next'. Dừng tìm kiếm.")
                        break
                else:
                    # Nếu chưa ở cuối trang, cuộn ngẫu nhiên
                    scroll_distance = random.randint(300, 400)
                    print(f"Không tìm thấy từ khóa, cuộn ngẫu nhiên {scroll_distance} pixel...")
                    self.mouse_controller.scroll(-scroll_distance)  # Cuộn xuống
                    time.sleep(1)  # Đợi một chút để nội dung tải lại
                    count_scroll += 1
                    # Cập nhật ảnh chụp màn hình sau khi cuộn
                    screenshot = pyautogui.screenshot(region=self.region)
                    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                    
        # Di chuyển đến vị trí top-right của ảnh và click
        top_right_x = screenshot.shape[1] - 5
        top_right_y = 5
        self.mouse_controller.move_to(top_right_x, top_right_y, duration=0.2)
        self.mouse_controller.click()
        print(f"Đã click vào vị trí top-right: ({top_right_x}, {top_right_y}).")