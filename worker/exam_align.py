from alignment.align_matrix import ImageAlignment
import cv2

if __name__=="__main__":
  ref_path = "../images/target.png"
  obj_path = "../images/target_test1.jpg"

  alignment = ImageAlignment(1)
  
  ref_img = cv2.imread(ref_path, cv2.IMREAD_COLOR)
  obj_img = cv2.imread(obj_path, cv2.IMREAD_COLOR)
  
  matrix = alignment.getMatrix(obj_img, ref_img)
  
  height, width, channel = ref_img.shape
  warp_img = cv2.warpPerspective(obj_img, matrix, (width, height))

  outFilePath = "../results/aligned.jpg"
  cv2.imwrite(outFilePath, warp_img)

  cv2.imshow("Reference", ref_img)
  cv2.imshow("Object", obj_img)
  cv2.imshow("Warped Image", warp_img)
  
  cv2.waitKey()
  cv2.destroyAllWindows()

