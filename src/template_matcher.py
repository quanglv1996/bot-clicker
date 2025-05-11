import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui

class TemplateMatcher:
    def __init__(self):
        """
        Khởi tạo TemplateMatcher.
        """
        pass

    def matcher(self, image, template_image, threshold=0.5, scales=np.linspace(0.2, 5, 40)):
        """
        Nhận diện template trên ảnh với nhiều kích thước khác nhau.
        :param image: Ảnh đầu vào (NumPy array).
        :param template_image: Ảnh template (NumPy array).
        :param threshold: Ngưỡng để xác định khớp (mặc định là 0.5).
        :param scales: Các tỷ lệ phóng to/thu nhỏ để thử nghiệm.
        :return: Tọa độ trung tâm của template nếu tìm thấy, None nếu không tìm thấy.
        """
        print("Đang tìm template trên ảnh với nhiều kích thước...")

        # Chuyển ảnh đầu vào và template sang grayscale
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
        template_h, template_w = template_gray.shape[:2]

        best_match = None
        best_val = 0

        # Duyệt qua các tỷ lệ
        for scale in scales:
            resized_template = cv2.resize(template_gray, (int(template_w * scale), int(template_h * scale)))
            result = cv2.matchTemplate(image_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Kiểm tra nếu điểm khớp tốt hơn ngưỡng và tốt nhất hiện tại
            if max_val > threshold and max_val > best_val:
                best_val = max_val
                best_match = (max_loc, resized_template.shape[1], resized_template.shape[0])

        if best_match:
            top_left, w, h = best_match
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            print(f"Đã tìm thấy template tại tọa độ: ({center_x}, {center_y}) với độ khớp: {best_val:.2f}")
            return center_x, center_y
        else:
            print("Không tìm thấy template.")
            return None


def main():
    """
    Chương trình chính để tìm và click vào template.
    """
    # Đường dẫn đến template icon Google
    GOOGLE_ICON_TEMPLATE = r"D:\bot-clicker\assets\google_icon.JPG"

    # Đọc template icon Google
    template_image = cv2.imread(GOOGLE_ICON_TEMPLATE)

    # Khởi tạo TemplateMatcher
    matcher = TemplateMatcher()

    # Chụp ảnh màn hình
    screenshot = ImageGrab.grab(all_screens=True)
    screenshot_np = np.array(screenshot)

    # Tìm kiếm template trên ảnh
    icon_position = matcher.matcher(screenshot_np, template_image, threshold=0.5, scales=np.linspace(0.2, 5, 40))

    if icon_position:
        # Di chuyển chuột đến icon và click
        pyautogui.moveTo(icon_position[0], icon_position[1], duration=.2)
        pyautogui.click()
        print("Đã click vào template.")
    else:
        print("Không thể thực hiện click vì không tìm thấy template.")


if __name__ == "__main__":
    main()