import cv2

class Picture(object):
    def __init__(self, source):
        self._source = source

    def takePic(self, path):
        # /dev/video0
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        cv2.imshow("frame", frame)
        cv2.waitKey(0)
        # Setting file path & format 
        outputFile = path + ".jpg"
        # Save image
        cv2.imwrite(outputFile, frame)



