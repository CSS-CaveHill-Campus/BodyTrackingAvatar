import cv2 
import sys
import numpy as np
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from client import client


base_options = python.BaseOptions(model_asset_path='pose_landmarker_lite.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
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
    return annotated_image


def main():
    webcam = cv2.VideoCapture(0)
    while webcam.isOpened():
        success, img = webcam.read()
        img = cv2.flip(img, 1)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

        detection_result = detector.detect(mp_img)

        annotated_image = draw_landmarks_on_image(mp_img.numpy_view(), detection_result)

        cv2.imshow("Live Gesture Viewer", annotated_image)

        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

    return webcam

if __name__ == "__main__":
    try:
        webcam = main()
    except KeyboardInterrupt:
        pass 
    finally:
        if (webcam):
            webcam.release()
        cv2.destroyAllWindows()
        client.disconnect()
        sys.exit(1)
