# ORIGINAL FOTO
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

# Load the image
img = cv2.imread('image4.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Display the grayscale image
plt.imshow(gray, cmap='gray')
plt.axis('off')
plt.show()

# Noise reduction
bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

# Edge detection
edged = cv2.Canny(bfilter, 30, 200)

# Display the edge-detected image
plt.imshow(edged, cmap='gray')
plt.axis('off')
plt.show()

# Find contours in the edged image
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None

# Loop over the contours
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break

# Create a mask
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0, 255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)

# Display the masked image
plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# Find coordinates of the bounding box
(x, y) = np.where(mask == 255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))

# Crop the image
cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

# Display the cropped image
plt.imshow(cropped_image, cmap='gray')
plt.axis('off')
plt.show()

# Perform OCR on the cropped image
reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)

# Extract the text
text = result[0][-2]

# Draw the text and bounding box on the original image
font = cv2.FONT_HERSHEY_SIMPLEX
res = cv2.putText(img, text=text, org=(location[0][0][0], location[1][0][1] + 60), fontFace=font, fontScale=1,
                  color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
res = cv2.rectangle(img, tuple(location[0][0]), tuple(location[2][0]), (0, 255, 0), 3)

# Display the final result
plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
