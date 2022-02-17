import cv2

from capture import Picture
from align_matrix import ImageAlignment
from yolov5.detect import ObjectDetection
    
if __name__=="__main__":
    # Take a picture
    pic = Picture(None)
    path = "/home/pi/ShotTracker/integrated/images/capture/taken"
    pic.takePic(path)
    
    print("take a picture")

    ref_path = "/home/pi/ShotTracker/integrated/images/reference/refer"
    obj_path = path

    # Warp captured image
    alignment = ImageAlignment(None)
    ref_img = cv2.imread(ref_path+".jpeg", cv2.IMREAD_COLOR)
    obj_img = cv2.imread(obj_path+".jpeg", cv2.IMREAD_COLOR)

    matrix = alignment.getMatrix(obj_img, ref_img)
    height, width, channel = ref_img.shape
    warp_img = cv2.warpPerspective(obj_img, matrix, (width, height))

    outFilePath = "/home/pi/ShotTracker/integrated/images/warped/warped"
    cv2.imwrite(outFilePath+".jpeg", warp_img)

    print("image warping")

    # Object Detection
    yolo = ObjectDetection(None)
    bullets = yolo.run()

    print(bullets)
