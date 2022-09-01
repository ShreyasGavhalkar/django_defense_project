import os
import cv2
import numpy as np
import math
import mediapipe as mp
from time import time
import os
from datetime import datetime


# Build Keypoints using MP Holistic
mp_holistic = mp.solutions.holistic      # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR CONVERSION RGB 2 BGR
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(
        image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)  # Draw face connections
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)  # Draw pose connections
    mp_drawing.draw_landmarks(
        image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw left hand connections
    mp_drawing.draw_landmarks(
        image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)  # Draw right hand connections

def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(
        image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
        mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
        mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1))
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2))
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

def run_mediapipe_holistic(frame):
    with mp_holistic.Holistic(min_detection_confidence=0.3, min_tracking_confidence=0.3,static_image_mode=False) as holistic: #static_image=True
        image, results = mediapipe_detection(frame, holistic)
        draw_landmarks(image, results)
        return results, image


def get_angle(landmark1, landmark2, landmark3):
    """Returns angle between the two vectors formed by the passed three points"""
    flag=False
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


    return  angle

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


def image_check(results, image2):
    """Returns a frame with specific landmarks plotted , calculated angle value and flag indicating if slatue was correct"""
    
    angle = -1 #provide default value
    angle_flag=False
    salute_flag = False
    if results.face_landmarks is None: # Checking face, body, right hand and left hand visisbility
        image2 = cv2.putText(image2, "Face Not Visible", (270, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    if results.pose_landmarks is None:
        image2 = cv2.putText(image2, "Body Not Visible", (270, 390), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    #if results.left_hand_landmarks is None:
        #image2 = cv2.putText(image2, "Left Hand Not Visible", (270, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    if results.right_hand_landmarks is None:
        image2 = cv2.putText(image2, "Right Hand Not Visible", (270, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    if results.face_landmarks and results.pose_landmarks and results.right_hand_landmarks:
        f = results.face_landmarks.landmark[130]  # eyebrow face
        s = results.pose_landmarks.landmark[12]  # shoulder
        e = results.pose_landmarks.landmark[14]  # elbow
        w = results.pose_landmarks.landmark[16]  # wrist
        h = results.right_hand_landmarks.landmark[12]  # hand =>middle finger
        h2 = results.right_hand_landmarks.landmark[11]

        height, width, channels = image2.shape
        f_x, f_y = int(f.x * width), int(f.y * height)
        s_x, s_y = int(s.x * width), int(s.y * height)
        e_x, e_y = int(e.x * width), int(e.y * height)
        w_x, w_y = int(w.x * width), int(w.y * height)

        h_x, h_y = int(h.x * width), int(h.y * height)
        h2_x, h2_y = int(h2.x * width), int(h2.y * height)

        image2 = cv2.circle(image2, (f_x, f_y), radius=2, color=(0, 0, 255), thickness=-1)
        image2 = cv2.circle(image2, (s_x, s_y), radius=2, color=(0, 0, 255), thickness=-1)
        image2 = cv2.circle(image2, (e_x, e_y), radius=2, color=(0, 0, 255), thickness=-1)
        image2 = cv2.circle(image2, (w_x, w_y), radius=2, color=(0, 0, 255), thickness=-1)
        image2 = cv2.circle(image2, (h_x, h_y), radius=2, color=(0, 0, 255), thickness=-1)
        image2 = cv2.circle(image2, (h2_x, h2_y), radius=2, color=(0, 0, 255), thickness=-1)

        angle = get_angle((s_x, s_y), (e_x, e_y), (w_x, w_y))
        # dist = get_distance((f_x, f_y), (h_x, h_y)) <= 1.75 * get_distance((h_x, h_y), (h2_x, h2_y))
        #TODO : change this value
        dist = get_distance((f_x, f_y), (h_x, h_y)) <= 1.75 * get_distance((h_x, h_y), (h2_x, h2_y))
        # print(get_distance((h_x, h_y), (f_x, f_y)))
        # print(1.75 * get_distance((h_x, h_y), (h2_x, h2_y)))
        # image2 = cv2.flip(image2, 1)

        image2 = cv2.putText(image2, f'Angle - {angle_flag} {round(angle,1)}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 250), 2)

        #TODO : change this value
        if angle >= 310 and angle < 322:  # To be true angle should be between 40-60 degrees
            angle_flag=True

        if angle_flag:
            if dist:
                image2 = cv2.putText(image2, f'Salute correct', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
                image2 = cv2.putText(image2, f'Distance - {dist}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
                image2 = cv2.putText(image2, f'Angle - {angle_flag} {round(angle,1)}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
            
            else:
                image2 = cv2.putText(image2, f'Salute Incorrect', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2)
                image2 = cv2.putText(image2, f'Distance - {dist}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2)
                # image2 = cv2.putText(image2, f'Angle - {angle_flag} {round(angle,1)}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2)
    else:
        print('Please ensure full body is visible before the screen')

    if angle_flag and dist:
        salute_flag=True

    return image2, angle,salute_flag

def main():

    cp = cv2.VideoCapture(0)
    cp.set(cv2.CAP_PROP_FRAME_WIDTH, 1100)
    cp.set(cv2.CAP_PROP_FRAME_HEIGHT, 1100)
    frame_width = int(cp.get(3))
    frame_height = int(cp.get(4))
    correct=0       #Flag for if correct salute was detected in the video atleast once.
    last_flag = False  #Flag to check if the coreect salute detected was the first instance.
    today=datetime.now().strftime("%Y_%m_%d-%I_%H_%M_%S")
    iwriter = cv2.VideoWriter(f'ProcessedVideo_{today}.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, (frame_width, frame_height)) #writes for default starting 5 sec
    swriter = cv2.VideoWriter(f'ProcessedVideo_salute_{today}.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (frame_width, frame_height)) #writer for when correct salute is detected


    start = time()


    while True:
        frame_counter = 0
        ok, frame = cp.read()
        # frame = cv2.resize (frame, (1220, 680))
        end=time()
        # frame = cv2.flip(frame, 1)
        if not ok:
            print('Video Over or not accessible')
            break
        # if frame_counter % 3 == 0:
        #Allowing only every 3rd frame to be processed
        frame = cv2.blur(frame, (3, 3))
        results, frame = run_mediapipe_holistic(frame)
        image2,angle,salute_flag = image_check(results, frame)
        # cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('frame', image2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


        if end-start<=20 and not correct:
            iwriter.write(image2)
        # print(f'salute flag is {salute_flag}')


        if salute_flag and not correct:
                correct=1
                last_flag=True
                start_angle = time()


        if last_flag :
            if time() - start_angle <= 20:
                swriter.write(image2)
                # print(f'fame written to swriter at time of {time() - start_angle}')
            
            # frame_counter += 1

    cp.release()
    cv2.destroyAllWindows()
    iwriter.release()
    swriter.release()
    if correct==1:
        os.remove(f'ProcessedVideo_{today}.avi')
    elif correct==0:
        os.remove(f'ProcessedVideo_salute_{today}.avi')

main()