#============================ IMPORTS ===================================
import cv2
import math
import os
import mediapipe as mp
import pdb
from PIL import Image
from io import BytesIO
import base64
import numpy as np

#============================= Model Loading and detection =============================

mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR CONVERSION RGB 2 BGR
    return image, results

#================================== Drawing Landmarks ==================================

def draw_pose_landmarks(image, results):
     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)  # Draw pose connections

def draw_styled_pose_landmarks(image,results):
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))

def draw_hand_landmarks(image,results):
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw right hand connections

def draw_styled_hand_landmarks(image, results):
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

def draw_face_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)  # Draw face connections

def draw_styled_face_landmarks(image, results):
     # Draw face connections
    mp_drawing.draw_landmarks(
        image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
        mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
        mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1))

#================================== Pose Check ==================================

def salute_check(landmark1, landmark2, landmark3):

    # Get the required landmarks coordinates.
    x1, y1 = landmark1
    x2, y2 = landmark2
    x3, y3 = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

    # Check if the angle is less than zero.
    if angle < 0:
        # Add 360 to the found angle.
        angle += 360
    if angle >= 300 and angle < 320:
        return True, angle

    return False, angle

def get_distance(p, q):
    """
    Return euclidean distance between points p and q
    assuming both to have the same number of dimensions
    """
    # sum of squared difference between coordinates
    s_sq_difference = 0
    for p_i, q_i in zip(p, q):
        s_sq_difference += (p_i - q_i) ** 2

    # take sq root of sum of squared difference
    distance = s_sq_difference ** 0.5
    return distance

def get_coordinates(results,image):
    f = results.face_landmarks.landmark[130]  # eyebrow face
    s = results.pose_landmarks.landmark[12]  # shoulder
    e = results.pose_landmarks.landmark[14]  # elbow
    w = results.pose_landmarks.landmark[16]  # wrist
    h = results.right_hand_landmarks.landmark[12]  # hand =>index middle finger
    h2 = results.right_hand_landmarks.landmark[11]

    height, width, channels = image.shape

    right_eyebrow_face = int(f.x * width), int(f.y * height)
    right_shoulder = int(s.x * width), int(s.y * height)
    rightelbow = int(e.x * width), int(e.y * height)
    rightwrist = int(w.x * width), int(w.y * height)
    right_hand_middle_finger_tip = int(h.x * width), int(h.y * height)
    right_hand_middle_finger_section2 = int(h2.x * width), int(h2.y * height)

    return right_eyebrow_face, right_shoulder, rightelbow, rightwrist, right_hand_middle_finger_tip, right_hand_middle_finger_section2


def image_check(results, image2):
    # Get the required landmarks coordinates.
    right_eyebrow_face, right_shoulder, rightelbow, rightwrist, right_hand_middle_finger_tip, right_hand_middle_finger_section2 = get_coordinates(results, image2)

    #BGR format for colors
    image2 = cv2.circle(image2, (right_eyebrow_face[0], right_eyebrow_face[1]), radius=10, color=(0, 255, 255), thickness=-1)
    image2 = cv2.circle(image2, (right_shoulder[0], right_shoulder[1]), radius=10, color=(0, 255, 255), thickness=-1)
    image2 = cv2.circle(image2, (rightelbow[0], rightelbow[1]), radius=10, color=(0, 255, 255), thickness=-1)
    image2 = cv2.circle(image2, (rightwrist[0], rightwrist[1]), radius=10, color=(0, 255, 255), thickness=-1)
    image2 = cv2.circle(image2, (right_hand_middle_finger_tip[0], right_hand_middle_finger_tip[1]), radius=10, color=(0, 255, 255), thickness=-1)
    image2 = cv2.circle(image2, (right_hand_middle_finger_section2[0], right_hand_middle_finger_section2[1]), radius=10, color=(0, 255, 255), thickness=-1)

    cv2.line(image2, rightelbow, right_shoulder, (0, 0, 255), thickness=2)
    cv2.line(image2, rightelbow, rightwrist, (0, 0, 255), thickness=2)
    cv2.line(image2, right_hand_middle_finger_tip, right_hand_middle_finger_section2, (0, 255, 0), thickness=2)
    cv2.line(image2, right_hand_middle_finger_tip, right_eyebrow_face, (0, 255, 0), thickness=2)

    flag, angle = salute_check((right_shoulder), (rightelbow), (rightwrist))
    dist = get_distance((right_eyebrow_face), (right_hand_middle_finger_tip)) <= 1.75 * get_distance((right_hand_middle_finger_tip), (right_hand_middle_finger_section2))


    if flag:
        image2 = cv2.putText(image2, 'Salute correct', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                             cv2.LINE_AA)
    if dist:
        image2 = cv2.putText(image2, 'Distance Correct', (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                             cv2.LINE_AA)

    return image2, angle, dist, flag

#================================== Execution ==================================

def main(image_data):
    #pdb.set_trace()
    frame = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
    print(frame)

    with mp_holistic.Holistic(static_image_mode=True, model_complexity=1, refine_face_landmarks=True) as holistic:
        image, results = mediapipe_detection(frame, holistic)

    if results.pose_landmarks:
        image2 = image.copy()
        draw_styled_pose_landmarks(image2, results)
        # cv2.imshow('Pose Landmarks', image2)
        #TODO 1: add visibility logic here
        image, angle, dist, flag = image_check(results, frame)
        print(f'Angle is {angle}')
        if flag and dist:
            return ['Activity Passed', angle]
    
    # cv2.imshow('image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite('/media/Output.jpg', image)

# main(r"/home/shreyas/Documents/Code/django_project/django_defense_project/defense_project/defense/static/defense/salute.jpeg")
def run(b64string):
    f = BytesIO()
    # b64string = ""
    f.write(base64.b64decode(b64string))
    f.seek(0)
    image =  Image.open(f)
    npImg = np.array(image)
    try:
        return main(npImg)
    except:
        return ['Activity Failed', 0]


#Things to verify:
#1. Model complexity does not run on my machine (atharva) [check this for raspberry pi]
