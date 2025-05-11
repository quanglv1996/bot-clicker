import pyautogui
import random
import time
import math
import numpy as np

class MouseController:
    def __init__(self):
        pass

    def move_to(self, x, y, duration=.2):
        """
        Di chuyển chuột đến tọa độ (x, y) bằng cách chọn ngẫu nhiên một trong các phương pháp di chuyển.
        :param x: Tọa độ x trên màn hình
        :param y: Tọa độ y trên màn hình
        :param duration: Thời gian di chuyển đến đích (giây)
        """
        # Danh sách các phương pháp di chuyển
        methods = [
            self._move_linear,
            self._move_smoothstep,
            self._move_zigzag,
            self._move_wave,
        ]

        # Chia thời gian di chuyển thành các đoạn nhỏ
        num_segments = random.randint(1, 2)  # Số đoạn di chuyển (ngẫu nhiên từ 2 đến 4)
        segment_duration = duration / num_segments

        # Lấy vị trí bắt đầu
        start_x, start_y = pyautogui.position()

        # Tính tọa độ trung gian cho từng đoạn
        intermediate_points = [(start_x, start_y)]
        for _ in range(num_segments - 1):
            intermediate_x = random.uniform(start_x, x)
            intermediate_y = random.uniform(start_y, y)
            intermediate_points.append((intermediate_x, intermediate_y))
        intermediate_points.append((x, y))  # Thêm điểm cuối

        # Di chuyển qua từng đoạn với phương pháp ngẫu nhiên
        for i in range(len(intermediate_points) - 1):
            method = random.choice(methods)  # Chọn phương pháp ngẫu nhiên
            start = intermediate_points[i]
            end = intermediate_points[i + 1]
            method(end[0], end[1], random.uniform(segment_duration/2, segment_duration))

    def _add_gaussian_noise(self, value, stddev=1):
        """Thêm nhiễu Gaussian vào giá trị."""
        return value + np.random.normal(0, stddev)

    def _move_linear(self, x, y, duration=0.2):
        """Di chuyển theo đường thẳng với nhiễu Gaussian."""
        start_x, start_y = pyautogui.position()
        steps = random.randint(5, 10)
        for i in range(steps):
            t = i / steps
            current_x = start_x + (x - start_x) * t
            current_y = start_y + (y - start_y) * t
            # Thêm nhiễu Gaussian
            current_x = self._add_gaussian_noise(current_x, stddev=2)
            current_y = self._add_gaussian_noise(current_y, stddev=2)
            pyautogui.moveTo(current_x, current_y, duration=(duration / steps))
        pyautogui.moveTo(x, y)

    def _move_smoothstep(self, x, y, duration):
        """Di chuyển theo quỹ đạo mượt mà (smoothstep) với nhiễu Gaussian."""
        start_x, start_y = pyautogui.position()
        steps = random.randint(5, 10)
        for i in range(steps):
            t = i / steps
            ease_t = t * t * (3 - 2 * t)
            current_x = start_x + (x - start_x) * ease_t
            current_y = start_y + (y - start_y) * ease_t
            # Thêm nhiễu Gaussian
            current_x = self._add_gaussian_noise(current_x, stddev=2)
            current_y = self._add_gaussian_noise(current_y, stddev=2)
            pyautogui.moveTo(current_x, current_y, duration=(duration / steps))
        pyautogui.moveTo(x, y)

    def _move_zigzag(self, x, y, duration):
        """Di chuyển theo quỹ đạo zigzag với nhiễu Gaussian."""
        start_x, start_y = pyautogui.position()
        steps = random.randint(5, 10)
        for i in range(steps):
            t = i / steps
            offset = 10 * (-1 if i % 2 == 0 else 1)  # Zigzag offset
            current_x = start_x + (x - start_x) * t
            current_y = start_y + (y - start_y) * t + offset
            # Thêm nhiễu Gaussian
            current_x = self._add_gaussian_noise(current_x, stddev=2)
            current_y = self._add_gaussian_noise(current_y, stddev=2)
            pyautogui.moveTo(current_x, current_y, duration=(duration / steps))
        pyautogui.moveTo(x, y)

    def _move_random_curve(self, x, y, duration):
        """Di chuyển theo quỹ đạo đường cong ngẫu nhiên với nhiễu Gaussian."""
        start_x, start_y = pyautogui.position()
        control_x = random.uniform(start_x, x)
        control_y = random.uniform(start_y, y)
        steps = random.randint(5, 10)
        for i in range(steps):
            t = i / steps
            current_x = (1 - t) ** 2 * start_x + 2 * (1 - t) * t * control_x + t ** 2 * x
            current_y = (1 - t) ** 2 * start_y + 2 * (1 - t) * t * control_y + t ** 2 * y
            # Thêm nhiễu Gaussian
            current_x = self._add_gaussian_noise(current_x, stddev=2)
            current_y = self._add_gaussian_noise(current_y, stddev=2)
            pyautogui.moveTo(current_x, current_y, duration=(duration / steps))
        pyautogui.moveTo(x, y)

    def _move_wave(self, x, y, duration):
        """Di chuyển theo quỹ đạo sóng với nhiễu Gaussian."""
        start_x, start_y = pyautogui.position()
        steps = random.randint(5, 10)
        amplitude = 20  # Biên độ sóng
        frequency = 5  # Tần số sóng
        for i in range(steps):
            t = i / steps
            current_x = start_x + (x - start_x) * t
            current_y = start_y + (y - start_y) * t + amplitude * math.sin(frequency * t * 2 * math.pi)
            # Thêm nhiễu Gaussian
            current_x = self._add_gaussian_noise(current_x, stddev=2)
            current_y = self._add_gaussian_noise(current_y, stddev=2)
            pyautogui.moveTo(current_x, current_y, duration=(duration / steps))
        pyautogui.moveTo(x, y)

    def click(self):
        """Click chuột trái tại vị trí hiện tại."""
        pyautogui.click()

    def double_click(self):
        """Click đúp chuột trái tại vị trí hiện tại."""
        pyautogui.doubleClick()

    def scroll(self, n):
        """Cuộn chuột với chiều dài n pixel."""
        pyautogui.scroll(n)


# Sử dụng lớp MouseController
if __name__ == "__main__":
    mouse = MouseController()

    # Di chuyển chuột đến tọa độ (500, 500) trong 2 giây
    mouse.move_to(500, 500, duration=.2)

    # Click chuột trái
    mouse.click()

    # Click đúp chuột trái
    mouse.double_click()

    # Cuộn chuột xuống 300 pixel
    mouse.scroll(-300)

    # Cuộn chuột lên 300 pixel
    mouse.scroll(300)