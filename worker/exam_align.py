from alignment.align_matrix import ImageAlignment
import cv2
def align(ref,obj):
  refROOT = os.environ.get("REFER_IMAGE_DIRECTORY", Path(os.path.relpath(ROOT, Path.cwd())) ) # relative
  resROOT = os.environ.get("SOURCE_IMAGE_DIRECTORY", Path(os.path.relpath(ROOT, Path.cwd())) ) # relative

  ref_path = refROOT+"/"+ref+".jpg"
  obj_path = resROOT+"/"+obj+".jpg"

  alignment = ImageAlignment(1)
  
  ref_img = cv2.imread(ref_path, cv2.IMREAD_COLOR)
  obj_img = cv2.imread(obj_path, cv2.IMREAD_COLOR)
  
  matrix = alignment.getMatrix(obj_img, ref_img)

  height, width, channel = ref_img.shape
  warp_img = cv2.warpPerspective(obj_img, matrix, (width, height))

  outFilePath = os.environ.get("WARP_IMAGE_DIRECTORY", Path(os.path.relpath(ROOT, Path.cwd())) )+"/" +obj+".jpg"

  cv2.imwrite(outFilePath, warp_img)
  return matrix

if __name__=="__main__":
  align()


