# -*- coding: utf-8 -*-
# FILE: cv_logic.py
import face_recognition
import cv2
import dlib
import os
import numpy as np
from collections import deque

def calculate_iou(boxA, boxB):
    """Tính toán Intersection over Union (IoU) giữa hai bounding box."""
    # Chuyển đổi box (top, right, bottom, left) sang (left, top, right, bottom) để tính toán
    boxA_coords = (boxA[3], boxA[0], boxA[1], boxA[2])
    boxB_coords = (boxB[3], boxB[0], boxB[1], boxB[2])
    
    xA = max(boxA_coords[0], boxB_coords[0])
    yA = max(boxA_coords[1], boxB_coords[1])
    xB = min(boxA_coords[2], boxB_coords[2])
    yB = min(boxA_coords[3], boxB_coords[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA_coords[2] - boxA_coords[0]) * (boxA_coords[3] - boxA_coords[1])
    boxBArea = (boxB_coords[2] - boxB_coords[0]) * (boxB_coords[3] - boxB_coords[1])
    
    iou = interArea / float(boxAArea + boxBArea - interArea) if (boxAArea + boxBArea - interArea) > 0 else 0
    return iou

class CVLogic:
    def __init__(self):
        self.KNOWN_FACES_DIR = "known_faces"
        self.TOLERANCE = 0.35
        self.MODEL = "hog"
        self.CONFIRMATION_COUNT = 3

        self.known_faces_encodings = []
        self.known_faces_names = []
        # Cấu trúc tracker: [tracker, confirmed_name, history_deque]
        self.active_trackers = []
        self.checked_in_names = set()
        self.load_known_faces()

    def load_known_faces(self):
        """Tải hoặc tải lại dữ liệu khuôn mặt đã biết."""
        print("🔄 Đang tải lại dữ liệu khuôn mặt...")
        self.known_faces_encodings = []
        self.known_faces_names = []
        if not os.path.exists(self.KNOWN_FACES_DIR):
            os.makedirs(self.KNOWN_FACES_DIR)
        for name in os.listdir(self.KNOWN_FACES_DIR):
            person_dir = os.path.join(self.KNOWN_FACES_DIR, name)
            if not os.path.isdir(person_dir): continue
            for filename in os.listdir(person_dir):
                try:
                    image = face_recognition.load_image_file(os.path.join(person_dir, filename))
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        self.known_faces_encodings.append(encodings[0])
                        self.known_faces_names.append(name)
                except Exception as e:
                    print(f"❌ Lỗi ảnh {filename}: {e}")
        print(f"✅ Đã tải xong {len(self.known_faces_names)} khuôn mặt.")
        return True

    def reset_attendance(self):
        """Xóa danh sách điểm danh và các tracker."""
        self.checked_in_names.clear()
        self.active_trackers = []
        print("🔄 Danh sách điểm danh và các tracker đã được reset.")

    def process_frame_with_tracking(self, rgb_frame, frame_count, detection_interval=10):
        """Xử lý khung hình với logic xác nhận và quản lý vòng đời tracker."""
        
        # Cập nhật vị trí của các tracker hiện có
        for tracker_info in self.active_trackers:
            tracker_info[0].update(rgb_frame)

        # Chạy phát hiện định kỳ
        if frame_count % detection_interval == 0:
            # *** THAY ĐỔI: Tăng kích thước ảnh xử lý để nhận diện xa hơn ***
            resize_factor = 0.5 
            small_frame = cv2.resize(rgb_frame, (0, 0), fx=resize_factor, fy=resize_factor)
            # ***************************************************************
            
            face_locations = face_recognition.face_locations(small_frame, model=self.MODEL)
            
            # *** THAY ĐỔI: Cập nhật hệ số phóng to tương ứng ***
            scale = 1 / resize_factor
            scaled_locs = [(int(t*scale), int(r*scale), int(b*scale), int(l*scale)) for t,r,b,l in face_locations]
            # ***************************************************

            face_encodings = face_recognition.face_encodings(rgb_frame, scaled_locs)
            
            matched_tracker_indices = set()
            new_detections = []

            # Khớp các khuôn mặt mới với các tracker cũ
            for (top, right, bottom, left), face_encoding in zip(scaled_locs, face_encodings):
                detection_box = (top, right, bottom, left)
                name = "Guest"
                if self.known_faces_encodings:
                    face_distances = face_recognition.face_distance(self.known_faces_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if face_distances[best_match_index] < self.TOLERANCE:
                        name = self.known_faces_names[best_match_index]

                best_iou = 0
                best_tracker_idx = -1
                for i, (tracker, _, _) in enumerate(self.active_trackers):
                    pos = tracker.get_position()
                    tracker_box = (int(pos.top()), int(pos.right()), int(pos.bottom()), int(pos.left()))
                    iou = calculate_iou(detection_box, tracker_box)
                    if iou > best_iou:
                        best_iou = iou
                        best_tracker_idx = i
                
                if best_iou > 0.4 and best_tracker_idx not in matched_tracker_indices:
                    self.active_trackers[best_tracker_idx][2].append(name)
                    matched_tracker_indices.add(best_tracker_idx)
                else:
                    new_detections.append(((top, right, bottom, left), name))

            # Xóa các tracker không được khớp (người đã rời đi)
            unmatched_trackers = []
            for i, tracker_info in enumerate(self.active_trackers):
                if i not in matched_tracker_indices:
                    unmatched_trackers.append(tracker_info)
            for tracker_info in unmatched_trackers:
                self.active_trackers.remove(tracker_info)

            # Thêm các tracker mới cho các khuôn mặt không khớp
            for (top, right, bottom, left), name in new_detections:
                if left >= right or top >= bottom: continue
                tracker = dlib.correlation_tracker()
                rect = dlib.rectangle(left, top, right, bottom)
                tracker.start_track(rgb_frame, rect)
                history = deque([name], maxlen=self.CONFIRMATION_COUNT)
                self.active_trackers.append([tracker, "Guest", history])

        # Xử lý logic xác nhận và trả về kết quả
        results = []
        for tracker_info in self.active_trackers:
            tracker, confirmed_name, history = tracker_info
            display_name = history[-1] if history else confirmed_name
            is_confirmed = (len(history) == self.CONFIRMATION_COUNT) and (len(set(history)) == 1)
            
            status = "Confirming"
            if is_confirmed and display_name != "Guest":
                confirmed_name = display_name
                tracker_info[1] = confirmed_name
                if confirmed_name in self.checked_in_names:
                    status = "Checked-in"
                else:
                    status = "Recognized"
            elif confirmed_name != "Guest" and confirmed_name in self.checked_in_names:
                status = "Checked-in"
                display_name = confirmed_name

            pos = tracker.get_position()
            box = (int(pos.top()), int(pos.right()), int(pos.bottom()), int(pos.left()))
            results.append((box, display_name, status, confirmed_name))
            
        return results

