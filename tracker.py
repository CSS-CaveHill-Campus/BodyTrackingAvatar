import cv2 
import sys
import numpy as np
import mediapipe as mp
import json
import threading
from time import sleep
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


base_options = python.BaseOptions(model_asset_path='pose_landmarker_lite.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = rgb_image

    # Loop through the detected poses to visualize.
    landmark_lists = []
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
        annotated_image,
        pose_landmarks_proto,
        solutions.pose.POSE_CONNECTIONS,
        solutions.drawing_styles.get_default_pose_landmarks_style())
        landmark_lists.append(pose_landmarks_proto)
    return annotated_image, landmark_lists


webcam = cv2.VideoCapture(0)
def track(child_conn):
    while webcam.isOpened():
        success, img = webcam.read()
        img = cv2.flip(img, 1)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

        detection_result = detector.detect(mp_img)
        np_array_copy = np.copy(mp_img.numpy_view())
        annotated_image, landmarked_lists = draw_landmarks_on_image(np_array_copy, detection_result)
        
        if child_conn and detection_result.pose_landmarks:
            child_conn.send(landmarked_lists[0]) # This sends just the landmarks

        cv2.imshow("Live Gesture Viewer", annotated_image)

        if cv2.waitKey(5) & 0xFF == ord("q"):
            break
    print("Video Exited")

if __name__ == "__main__":
    track(None)
