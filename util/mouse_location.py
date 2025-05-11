import pyautogui
import time
from PIL import ImageGrab

class MouseLocation:
    def __init__(self):
        pass

    def track_mouse_with_screenshot(self):
        """
        Theo dõi vị trí chuột trên toàn bộ không gian màn hình mở rộng và hiển thị tọa độ x, y theo pixel từ ảnh màn hình.
        Nhấn Ctrl + C để dừng chương trình.
        """
        print("Di chuyển chuột để xem tọa độ pixel từ ảnh màn hình. Nhấn Ctrl + C để thoát.")
        try:
            while True:
                # Lấy vị trí hiện tại của chuột
                x, y = pyautogui.position()

                # Chụp ảnh toàn bộ không gian màn hình mở rộng
                screenshot = ImageGrab.grab(all_screens=True)

                # Lấy màu pixel tại vị trí chuột
                pixel_color = screenshot.getpixel((x, y))

                # Hiển thị tọa độ và màu pixel
                print(f"Tọa độ chuột: x={x}, y={y}, Màu pixel: {pixel_color}", end="\r")
                time.sleep(0.1)  # Giảm tần suất cập nhật để tránh quá tải
        except KeyboardInterrupt:
            print("\nĐã dừng theo dõi vị trí chuột.")

# Sử dụng lớp MouseLocation
if __name__ == "__main__":
    mouse_tracker = MouseLocation()
    mouse_tracker.track_mouse_with_screenshot()