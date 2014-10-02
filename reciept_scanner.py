#include dropbox sdk
import dropbox
from transform import four_point_transform
import imutils
from skimage.filter import threshold_adaptive
import numpy as np 
import argparse
import cv2
import subprocess
import datetime
import json
from pywatch import watcher
from os.path import exists


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to image file")
args = vars(ap.parse_args())



#app key/secret
app_key = 'zc9f0m94h290l55'
app_secret = 'vawochbctgwbtol'
access_type = 'Dropbox'
if(exists('access_file.txt')):
	access_file = open('access_file.txt', 'r')
else:
	access_file = open('access_file.txt', 'w+')

if(access_file.readline() == ""):
	

	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key,app_secret)

#
	authorize_url = flow.start()

	print '1. Go to: ' + authorize_url
	print '2. Click "Allow" (logged in)'
	print '3. Copy the authorization code.'
	code = raw_input("Enter the authorization code here: ").strip()

	access_token, user_id = flow.finish(code)
	access_file = open('access_file.txt','w')
	access_file.write("%s" % (access_token))
	access_file.close()
else:
	access_file = open('access_file.txt','r')
	access_token = access_file.readline()
	access_file.close()

client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

try:
	resp_fold_creation = client.file_create_folder('/reciepts_photos')
	resp_fold_creation = client.file_create_folder('/receipts_text')
except Exception:
	pass




image = cv2.imread(args["image"])
ratio = image.shape[0]/500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(gray, 75, 200)

print "Step 1 : Edge Detection"
#cv2.imshow("Image", image)
#cv2.imshow("Edged", edged)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

for c in cnts:
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	if(len(approx) == 4):
		screenCnt = approx
		break
		

print "STEP 2: find contours"
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
#cv2.imshow("Outline", image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

warped = four_point_transform(orig, screenCnt.reshape(4,2) * ratio)

warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped, 250, offset = 10)
warped = warped.astype("uint8") *255

print "Step 3: apply perspective transform"
#cv2.imshow("Original", imutils.resize(orig, height = 650))
#cv2.imshow("Scanned", imutils.resize(warped, height = 650))
#cv2.waitKey(0)
cv2.imwrite("warped.png", warped)

print("Step 4: Apply OCR")
cmd = ["C:/Program Files (x86)/Tesseract-OCR/tesseract.exe", "warped.png", "rec"]

process = subprocess.Popen(cmd, stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
outputstring = process.communicate()[0]

openFile = open('rec.txt','r')
file_upload_resp = client.put_file("/receipts_text/rec.txt", openFile)
openFile.close()

print('done hooray')