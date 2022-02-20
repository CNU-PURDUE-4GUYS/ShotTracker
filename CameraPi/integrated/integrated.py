import cv2
import numpy as np
import os

from yolov5.detect import ObjectDetection
    
if __name__=="__main__":
    # Take a picture
    cap = cv2.VideoCapture(0)
    cap.set(3, 1440)
    cap.set(4, 2160)

    ret, obj_img = cap.read()

    obj_path = "/home/pi/ShotTracker/integrated/images/capture/taken"
    cv2.imwrite(obj_path+".jpeg", obj_img)

    print("take a picture")
  
    # Get ref_img & obj_img
    #ref_path = "/home/pi/target/bullseye_large"
    ref_path = "/home/pi/ShotTracker/integrated/images/reference/refer"
    ref_img = cv2.imread(ref_path+".jpeg", cv2.IMREAD_COLOR)
    
    obj_gray = cv2.cvtColor(obj_img, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    
    MAX_NUM_FEATURES = 500

    orb = cv2.ORB_create(MAX_NUM_FEATURES)
    k1, d1 = orb.detectAndCompute(obj_gray, None)
    k2, d2 = orb.detectAndCompute(ref_gray, None)

    # Feature matching
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = list(matcher.match(d1, d2, None))

    # Eliminate features by distance
    matches.sort(key=lambda x: x.distance, reverse=False)

    numGoodMatches = int(len(matches) * 0.15) 

    matches = matches[:numGoodMatches]

    # Calculate warping matrix
    point1 = np.zeros((len(matches), 2), dtype=np.float32)
    point2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        point1[i, :] = k1[match.queryIdx].pt
        point2[i, :] = k2[match.trainIdx].pt

    # Get Matrix using library
    matrix, mask = cv2.findHomography(point1, point2, cv2.RANSAC)

    ref_img = cv2.imread(ref_path+".jpeg", cv2.COLOR_BGR2GRAY)
    height, width, channel = ref_img.shape

    warp_img = cv2.warpPerspective(obj_img, matrix, (width, height))

    warp_path = "/home/pi/ShotTracker/integrated/images/warped/warped"
    cv2.imwrite(warp_path+".jpeg", warp_img)

    print("image warping")

    # Object Detection
    yolo = ObjectDetection(None)
    bullets = yolo.run()

    print(bullets)
