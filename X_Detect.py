# -*- coding: utf-8 -*-
# Author: mihcuog@AILab
# Contatct: AI-Lab - Smart Things
# Detect HeadPen Wrong - Right - Video Detect
# First Detect Pen / Video Detect

import torch
import numpy as np
import cv2
from time import time
from ultralytics import YOLO
import os
from datetime import datetime
from playsound import playsound
import supervision as sv
import cvzone

class ObjectDetection:
    def __init__(self, capture_index):
        self.capture_index = capture_index
        self.email_sent = False
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
        self.model = self.load_model()
        self.CLASS_NAMES_DICT = self.model.model.names
        self.box_annotator = sv.BoxAnnotator(color=sv.ColorPalette.default(), thickness=1, text_thickness=None, text_scale=None)

    def load_model(self):
        model = YOLO("model_v3pt/best.pt")
        return model

    def predict(self, frame):
        results = self.model(frame)
        # print(results)
        return results
    
    # def imgwrite(self, img):
    #     now = datetime.now()
    #     current_time =now.strftime("%Y-%m-%d_%H_%M_%S")
    #     filename = '%s.png' % current_time
    #     cv2.imwrite(os.path.join(r"img_detect", filename), img)

    def draw_hexagon(self, frame, center_x, center_y,color=(0, 0, 255)):
        side_length = 100
        num_sides = 6
        hexagon_vertices = []
        for i in range(num_sides):
            x = int(center_x + side_length * np.cos(2 * np.pi * i / num_sides))
            y = int(center_y + side_length * np.sin(2 * np.pi * i / num_sides))
            hexagon_vertices.append((x, y))
            cv2.circle(frame, (x, y), 5, color , -1)
        for i in range(num_sides):
            start_point = hexagon_vertices[i]
            end_point = hexagon_vertices[(i + 1) % num_sides]
            cv2.line(frame, start_point, end_point, color, 2)
        hexagon_coordinates = np.array(hexagon_vertices)
        return frame, hexagon_coordinates

    def plot_bboxes(self, results, frame):
        xyxys = []
        confidences = []
        class_ids = []
        center_x1, center_y1 = 150, 170
        for result in results[0]:
            class_id = result.boxes.cls.cpu().numpy().astype(int)
            # print(result)
            if class_id == 0:
                xyxys.append(result.boxes.xyxy.cpu().numpy())
                confidences.append(result.boxes.conf.cpu().numpy())
                class_ids.append(result.boxes.cls.cpu().numpy().astype(int))
            else:
                xyxys.append(result.boxes.xyxy.cpu().numpy())
                confidences.append(result.boxes.conf.cpu().numpy())
                class_ids.append(result.boxes.cls.cpu().numpy().astype(int))
        detections = sv.Detections.from_ultralytics(results[0])
        frame = self.box_annotator.annotate(scene=frame, detections=detections)
        return frame, class_ids

    def __call__(self):
        cap = cv2.VideoCapture(self.capture_index)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        frame_count = 0
        mainCounter = cv2.imread("asset/true_right_bt.png", cv2.IMREAD_UNCHANGED)
        mainCounter = cv2.resize(mainCounter, (360, 180))
        # Tọa độ tâm của hình lục giác hiện tại
        frame_count_dung = 0
        frame_count_sai = 0
        center_x1, center_y1 = 150, 170
        while True:
            start_time = time()
            ret, frame = cap.read()
            assert ret
            frame, class_ids = self.plot_bboxes(self.predict(frame), frame)
            # Vẽ hình lục giác thứ nhất
            # print(class_ids)
            if 1 in class_ids:
                print("Ngoi But Bi Sai Huong")
                playsound(r'C:\new\Start-Up NaVin\All_ProjectS_Com\X_Project_ButBi\alerts\alert.wav')
                frame, hexagon_coordinates1 = self.draw_hexagon(frame, center_x1, center_y1,color=(0, 0, 255))
                # Tính toán tọa độ tâm của hình lục giác thứ hai (kế bên)
                center_x2 = center_x1 + 250  # Khoảng cách theo trục x
                center_y2 = center_y1
                frame_count_sai += 1 
                # print(frame_count_sai)
                # Vẽ hình lục giác thứ hai
                frame, hexagon_coordinates2 = self.draw_hexagon(frame, center_x2, center_y2, color=(0,0,255))
            else:
                frame, hexagon_coordinates1 = self.draw_hexagon(frame, center_x1, center_y1,color=(0, 255, 0))
            # Tính toán tọa độ tâm của hình lục giác thứ hai (kế bên)
                center_x2 = center_x1 + 250  # Khoảng cách theo trục x
                center_y2 = center_y1
                frame_count_dung += 1
                # print(frame_count_dung)
                # Vẽ hình lục giác thứ hai
                frame, hexagon_coordinates2 = self.draw_hexagon(frame, center_x2, center_y2, color=(0, 255, 0))
                # print("Ngoi But Bi Dung Huong")
            end_time = time()
            fps = 1/np.round(end_time - start_time, 2)
            frame = cvzone.overlayPNG(frame, mainCounter, (600, 0))
            cv2.putText(frame, f'True:{frame_count_dung}', (790, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            cv2.putText(frame, f'False:{frame_count_sai}', (790, 155), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            cv2.putText(frame, f'FPS:{int(fps)}', (610,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1)
            cv2.imshow('X_Detect - @minhcuong-AILab', frame)
            frame_count += 1
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

detector = ObjectDetection(capture_index="vid_test/butbi.mp4")
detector()
