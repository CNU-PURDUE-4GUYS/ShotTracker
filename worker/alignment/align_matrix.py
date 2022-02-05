import cv2
import numpy as np

class ImageAlignment(object):
  def __init__(self, source):
    self._source = source

  def getSource(self):
    return self._source

  def getMatrix(self, obj_img, ref_img):
    obj_gray = cv2.cvtColor(obj_img, cv2.COLOR_BGR2GRAY)    # img will be warped 
    ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)    # reference img

    MAX_NUM_FEATURES = 500                           # number of features
    
    # Get image's features using ORB
    orb = cv2.ORB_create(MAX_NUM_FEATURES)
    k1, d1 = orb.detectAndCompute(obj_gray, None)    # keypoints, descriptors
    k2, d2 = orb.detectAndCompute(ref_gray, None)

    # Features matching
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = list(matcher.match(d1, d2, None))

    # Eliminate features by distance
    matches.sort(key=lambda x: x.distance, reverse=False)

    numGoodMatches = int(len(matches) * 0.15)        # if image quality is bad, control this number
    matches = matches[:numGoodMatches]

    # Calculate warping matrix
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
      points1[i, :] = k1[match.queryIdx].pt
      points2[i, :] = k2[match.trainIdx].pt
    
    # Get Matrix using library
    matrix, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
    return matrix

