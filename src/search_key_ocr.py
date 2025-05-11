from doctr.io import DocumentFile
from doctr.models import ocr_predictor, from_hub
from PIL import Image, ImageDraw
import numpy as np
import re
import cv2
from datetime import datetime
import torch
class SearchKeyOCR(object):
    def __init__(self):
        reco_model = from_hub("Felix92/doctr-torch-parseq-multilingual-v1")
        # Kiểm tra xem có GPU hay không
        if torch.cuda.is_available():
            print("Sử dụng GPU để xây dựng mô hình.")
            self.model = ocr_predictor(
                det_arch='fast_base',
                reco_arch=reco_model,
                assume_straight_pages=True,
                detect_orientation=False,
                disable_crop_orientation=True,
                disable_page_orientation=True,
                straighten_pages=True,
                pretrained=True
            ).cuda().half()
        else:
            print("Sử dụng CPU để xây dựng mô hình.")
            self.model = ocr_predictor(
                det_arch='fast_base',
                reco_arch=reco_model,
                assume_straight_pages=True,
                detect_orientation=False,
                disable_crop_orientation=True,
                disable_page_orientation=True,
                straighten_pages=True,
                pretrained=True
            )
    
    def read_image(self, np_image):
        screenshot_bgr = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        path_save = 'temp.jpg'
        cv2.imwrite(path_save, screenshot_bgr)
        return path_save
    
    
    def normalize_text(self, text):
        """
        Chuẩn hóa văn bản bằng cách loại bỏ khoảng trắng và ký tự đặc biệt.
        :param text: Văn bản cần chuẩn hóa.
        :return: Văn bản đã được chuẩn hóa.
        """
        return re.sub(r'[^a-zA-Z0-9]', '', text).lower()


    def search_key(self, keyword="google", np_image=None, draw_bbox=False):
        """
        Tìm kiếm cụm từ và trả về trung tâm tọa độ của các vị trí chứa cụm từ.
        :param search_phrase: Cụm từ cần tìm kiếm.
        :return: Danh sách các tọa độ trung tâm [(page_idx, center_x, center_y), ...].
        """
        print("Thực hiện OCR trên ảnh ")
        docs = DocumentFile.from_images(self.read_image(np_image))
        # Sử dụng model OCR để nhận diện văn bản
        result = self.model(docs)
        # Chuẩn hóa từ khóa tìm kiếm
        normalized_search_phrase = self.normalize_text(keyword)

        matched_centers = []
        for page_idx, page in enumerate(result.pages):
            for block in page.blocks:
                for line in block.lines:
                    # Ghép tất cả các từ trong dòng thành một chuỗi và chuẩn hóa
                    line_text = " ".join([word.value for word in line.words])
                    normalized_line_text = self.normalize_text(line_text)

                    if normalized_search_phrase in normalized_line_text:  # Tìm kiếm cụm từ đã chuẩn hóa
                        # Tìm vị trí bắt đầu và kết thúc của cụm từ trong dòng
                        start_idx = normalized_line_text.find(normalized_search_phrase)
                        end_idx = start_idx + len(normalized_search_phrase)

                        # Lấy các từ liên quan đến cụm từ
                        matched_words = []
                        current_idx = 0
                        for word in line.words:
                            word_length = len(self.normalize_text(word.value))
                            if current_idx >= start_idx and current_idx + word_length <= end_idx:
                                matched_words.append(word)
                            current_idx += word_length

                        # Tính bounding box bao quanh cụm từ
                        if matched_words:
                            img_width, img_height = docs[page_idx].shape[1], docs[page_idx].shape[0]
                            x_min = int(matched_words[0].geometry[0][0] * img_width)
                            y_min = int(matched_words[0].geometry[0][1] * img_height)
                            x_max = int(matched_words[-1].geometry[1][0] * img_width)
                            y_max = int(matched_words[-1].geometry[1][1] * img_height)

                            # Tính trung tâm của bbox
                            center_x = (x_min + x_max) // 2
                            center_y = (y_min + y_max) // 2
                            matched_centers.append((page_idx + 1, center_x, center_y))
                            
                            if draw_bbox:
                                # Vẽ bounding box và tọa độ trung tâm lên ảnh bằng OpenCV
                                cv2.rectangle(np_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
                                center_text = f"({center_x}, {center_y})"
                                cv2.putText(np_image, center_text, (center_x, center_y - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        if draw_bbox:
            # Lưu ảnh với tên timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"output_{timestamp}.jpg"
            cv2.imwrite(output_path, np_image)
            print(f"Ảnh với bounding box đã được lưu tại: {output_path}")
                            
        return matched_centers


    def search_first_key(self, keyword="google", np_image=None, draw_bbox=False):
        """
        Tìm kiếm cụm từ và trả về tọa độ trung tâm của cụm từ đầu tiên từ trái sang phải, từ trên xuống dưới.
        :param keyword: Cụm từ cần tìm kiếm.
        :param np_image: Ảnh NumPy array cần tìm kiếm.
        :return: Tọa độ trung tâm và bounding box của cụm từ nếu tìm thấy, None nếu không tìm thấy.
        """
        print(f"Đang tìm cụm từ '{keyword}' xuất hiện đầu tiên trên màn hình...")
        print("Thực hiện OCR trên ảnh")
        docs = DocumentFile.from_images(self.read_image(np_image))
        result = self.model(docs)
        # Chuẩn hóa từ khóa tìm kiếm
        normalized_search_phrase = self.normalize_text(keyword)

        # Duyệt qua tất cả các từ được nhận diện
        for page_idx, page in enumerate(result.pages):
            for block in page.blocks:
                for line in block.lines:
                    # Ghép tất cả các từ trong dòng thành một chuỗi và chuẩn hóa
                    line_text = " ".join([word.value for word in line.words])
                    normalized_line_text = self.normalize_text(line_text)

                    if normalized_search_phrase in normalized_line_text:  # Tìm kiếm cụm từ đã chuẩn hóa
                        # Tìm vị trí bắt đầu và kết thúc của cụm từ trong dòng
                        start_idx = normalized_line_text.find(normalized_search_phrase)
                        end_idx = start_idx + len(normalized_search_phrase)

                        # Lấy các từ liên quan đến cụm từ
                        matched_words = []
                        current_idx = 0
                        for word in line.words:
                            word_length = len(self.normalize_text(word.value))
                            if current_idx >= start_idx and current_idx + word_length <= end_idx:
                                matched_words.append(word)
                            current_idx += word_length

                        # Tính bounding box bao quanh cụm từ
                        if matched_words:
                            img_width, img_height = np_image.shape[1], np_image.shape[0]
                            x_min = int(matched_words[0].geometry[0][0] * img_width)
                            y_min = int(matched_words[0].geometry[0][1] * img_height)
                            x_max = int(matched_words[-1].geometry[1][0] * img_width)
                            y_max = int(matched_words[-1].geometry[1][1] * img_height)

                            # Tính trung tâm của bbox
                            center_x = (x_min + x_max) // 2
                            center_y = (y_min + y_max) // 2
                            print(f"Đã tìm thấy cụm từ '{keyword}' tại tọa độ: ({center_x}, {center_y}) với bounding box: ({x_min}, {y_min}, {x_max}, {y_max})")
                            if draw_bbox:
                                # Vẽ bounding box và tọa độ trung tâm lên ảnh bằng OpenCV
                                cv2.rectangle(np_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
                                center_text = f"({center_x}, {center_y})"
                                cv2.putText(np_image, center_text, (center_x, center_y - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                output_path = f"output_{timestamp}_first_key.jpg"
                                cv2.imwrite(output_path, np_image)
                                print(f"Ảnh với bounding box đã được lưu tại: {output_path}")
                            
                            return (center_x, center_y), (x_min, y_min, x_max, y_max)

        print(f"Không tìm thấy cụm từ '{keyword}' trên màn hình.")
        return None, None
    
    
    def search_largest_bbox_key(self, keyword="google", np_image=None, draw_bbox=False):
        """
        Tìm kiếm cụm từ và trả về tọa độ trung tâm của bounding box có diện tích lớn nhất.
        :param keyword: Cụm từ cần tìm kiếm.
        :param np_image: Ảnh NumPy array cần tìm kiếm.
        :return: Tọa độ trung tâm và bounding box của cụm từ lớn nhất nếu tìm thấy, None nếu không tìm thấy.
        """
        print(f"Đang tìm cụm từ '{keyword}' có bounding box lớn nhất trên màn hình...")
        # Thực hiện OCR trên ảnh
        docs = DocumentFile.from_images(self.read_image(np_image))
        # Sử dụng model OCR để nhận diện văn bản
        result = self.model(docs)
        # Chuẩn hóa từ khóa tìm kiếm
        normalized_search_phrase = self.normalize_text(keyword)

        largest_area = 0
        largest_bbox = None
        largest_center = None

        # Duyệt qua tất cả các từ được nhận diện
        for page_idx, page in enumerate(result.pages):
            for block in page.blocks:
                for line in block.lines:
                    # Ghép tất cả các từ trong dòng thành một chuỗi và chuẩn hóa
                    line_text = " ".join([word.value for word in line.words])
                    normalized_line_text = self.normalize_text(line_text)

                    if normalized_search_phrase in normalized_line_text:  # Tìm kiếm cụm từ đã chuẩn hóa
                        # Tìm vị trí bắt đầu và kết thúc của cụm từ trong dòng
                        start_idx = normalized_line_text.find(normalized_search_phrase)
                        end_idx = start_idx + len(normalized_search_phrase)

                        # Lấy các từ liên quan đến cụm từ
                        matched_words = []
                        current_idx = 0
                        for word in line.words:
                            word_length = len(self.normalize_text(word.value))
                            if current_idx >= start_idx and current_idx + word_length <= end_idx:
                                matched_words.append(word)
                            current_idx += word_length

                        # Tính bounding box bao quanh cụm từ
                        if matched_words:
                            img_width, img_height = np_image.shape[1], np_image.shape[0]
                            x_min = int(matched_words[0].geometry[0][0] * img_width)
                            y_min = int(matched_words[0].geometry[0][1] * img_height)
                            x_max = int(matched_words[-1].geometry[1][0] * img_width)
                            y_max = int(matched_words[-1].geometry[1][1] * img_height)

                            # Tính diện tích của bounding box
                            area = (x_max - x_min) * (y_max - y_min)

                            # Cập nhật nếu diện tích lớn hơn giá trị lớn nhất hiện tại
                            if area > largest_area:
                                largest_area = area
                                largest_bbox = (x_min, y_min, x_max, y_max)
                                largest_center = ((x_min + x_max) // 2, (y_min + y_max) // 2)

        if largest_bbox:
            print(f"Đã tìm thấy cụm từ '{keyword}' có bounding box lớn nhất tại tọa độ: {largest_center} với bounding box: {largest_bbox}")
            if draw_bbox:
                # Vẽ bounding box và tọa độ trung tâm lên ảnh bằng OpenCV
                cv2.rectangle(np_image, (largest_bbox[0], largest_bbox[1]), (largest_bbox[2], largest_bbox[3]), (0, 0, 255), 2)
                center_text = f"({largest_center[0]}, {largest_center[1]})"
                cv2.putText(np_image, center_text, (largest_center[0], largest_center[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"output_{timestamp}_largest_bbox.jpg"
                cv2.imwrite(output_path, np_image)
                print(f"Ảnh với bounding box đã được lưu tại: {output_path}")
            return largest_center, largest_bbox

        print(f"Không tìm thấy cụm từ '{keyword}' trên màn hình.")
        return None, None

def main():
    # Sử dụng lớp SearchKey
    img = cv2.imread(r"D:\bot-clicker\temp1.jpg")
    search_key_tool = SearchKeyOCR()

    # Tìm kiếm cụm từ và trả về trung tâm tọa độ
    search_phrase = "o"
    centers = search_key_tool.search_key(search_phrase, img)
    print(f"Centers of the phrase '{search_phrase}': {centers}")
    img = cv2.imread(r"D:\bot-clicker\temp1.jpg")
    centers = search_key_tool.search_first_key(search_phrase, img)
    print(f"Centers of the phrase '{search_phrase}': {centers}")
    img = cv2.imread(r"D:\bot-clicker\temp1.jpg")
    centers = search_key_tool.search_largest_bbox_key(search_phrase, img)
    print(f"Centers of the phrase '{search_phrase}': {centers}")

if __name__ == "__main__":
    main()