from transform import four_point_transform
import np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to image file")
ap.add_argument("-c", "--coords", help = "comma seperated list of source pointer")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), dtype = "float32")

warped = four_point_transform(image, pts)

cv2.imshow("original", image)
cv2.imshow("warped", warped)
cv2.waitKey(0)