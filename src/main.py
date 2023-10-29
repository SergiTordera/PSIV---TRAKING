from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2
from math import dist
from centroidtracker import CentroidTracker
import time

AREA_THESHOLD = 15000
SIZE_X, SIZE_Y = 500, 400

def compute_substraction(frame, last_frames, window=10):
    img = frame[-SIZE_Y:, -SIZE_X:]
    img = cv2.resize(img,(600,500))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(35,35),0)
    last_frames.append(gray)
    if len(last_frames) > window:
        last_frames.pop(0)
    avg_frame = np.mean(last_frames, axis=0).astype('uint8')
    frameDelta = cv2.absdiff(avg_frame, gray)
    return img, frameDelta


def binarize_and_detection(frame, threshold_value=25, kernel_size=(7,3)):
    _,thresh = cv2.threshold(frame, threshold_value, 255, cv2.THRESH_BINARY)
    kernel = np.ones(kernel_size, np.uint8)
    thresh = cv2.dilate(thresh, None, iterations=6)
    contours, heirarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return contours


def process_contours(contours, img, debug=True):
    rectangles = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > AREA_THESHOLD:
            x,y,w,h = cv2.boundingRect(contour)
            box=(x,y,x+w,y+h)
            rectangles.append(box)
            if debug:
                cv2.rectangle(img,(x,y),(x+w,y+h),(128,0,255),3)
                cv2.putText(img,'CAR DETECTED',(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
    return rectangles


def track_positions(objects, positions, img, debug=True):
    for (objectID, centroid) in objects.items():
        if objectID not in list(positions.keys()):
            positions[objectID] = [centroid]
        else:
            positions[objectID].append(centroid)
        if debug:
            text = "ID {}".format(objectID)
            cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            cv2.putText(img, text, (centroid[0] - 10, centroid[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return positions


def compute_movements(positions):
    cars_up = 0
    cars_down = 0
    for k in positions.keys():
        start_y = positions[k][0][1]
        end_y = positions[k][-1][1]
        if start_y > end_y:
            cars_up += 1
        else:
            cars_down += 1
    return cars_up, cars_down


def main(path, debug=True):
    stream = cv2.VideoCapture(path)
    ct = CentroidTracker()
    original_fps = stream.get(cv2.CAP_PROP_FPS)
    double_fps = original_fps * 2
    stream.set(cv2.CAP_PROP_FPS, double_fps)

    fps = 0
    positions = {}
    last_frames = []

    while True:
        (grabbed, frame) = stream.read()
        if not grabbed:
            break
        
        img, frameDelta = compute_substraction(frame, last_frames=last_frames)
        if debug:
            cv2.imshow("Substraction", frameDelta)

        contours = binarize_and_detection(frame=frameDelta)
        rectangles = process_contours(contours=contours, img=img)
        objects = ct.update(rectangles)

        positions = track_positions(objects=objects, positions=positions, img=img)

        if debug:
            cv2.imshow('VIDEO',img)
            cv2.imshow('threshold',frameDelta)
            cv2.waitKey(10)
            cv2.putText(img, "Slow Method", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        fps+=1
        if fps % 2 == 0:
            stream.grab()
    #fps.stop()
    
    
    stream.release()
    cv2.destroyAllWindows()
    cup, cdown = compute_movements(positions=positions)
    print("CARS UP:  ", cup)
    print("CARS DOWN:  ", cdown)



if __name__ == "__main__":
    path_name = "output7.mp4"
    main(path=path_name)