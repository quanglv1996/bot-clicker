import pyautogui
import time
import random

class KeyboardController:
    def __init__(self):
        pass

    def type_text(self, text, delay_range=(0.05, 0.2)):
        """
        Nhập một chuỗi ký tự vào thanh tìm kiếm, mô phỏng như con người nhập từng ký tự.
        :param text: Chuỗi ký tự cần nhập
        :param delay_range: Khoảng thời gian ngẫu nhiên giữa các lần nhập ký tự (giây)
        """
        for char in text:
            pyautogui.typewrite(char)  # Nhập từng ký tự
            delay = random.uniform(*delay_range)  # Tạo độ trễ ngẫu nhiên
            time.sleep(delay)
        pyautogui.press("enter")  # Nhấn phím Enter sau khi nhập xong
        
    def press_enter(self):
        """
        Nhấn phím Enter.
        """
        pyautogui.press("enter")

# Sử dụng lớp KeyboardController
if __name__ == "__main__":
    keyboard = KeyboardController()

    # Chuỗi cần nhập vào thanh tìm kiếm
    search_query = "how to use Python"

    # Đợi vài giây để người dùng chuyển đến thanh tìm kiếm của Google
    print("Bạn có 5 giây để chuyển đến thanh tìm kiếm của Google...")
    time.sleep(5)

    # Nhập chuỗi vào thanh tìm kiếm và nhấn Enter
    keyboard.type_text(search_query)
    print("Đã nhập xong chuỗi tìm kiếm và nhấn Enter.")