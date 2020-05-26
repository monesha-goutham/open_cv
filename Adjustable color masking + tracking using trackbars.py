import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# q colour mask to show objects with specific colour according to our adjustments

def nothing(x):
    pass

#create sep window for the trackbar
cv2.namedWindow("trackbars")

#create trackbars for the lower and upper lims
l_h = cv2.createTrackbar("l-h","trackbars", 0, 179, nothing )
l_s = cv2.createTrackbar("l-s","trackbars", 0, 255, nothing )
l_v = cv2.createTrackbar("l-v","trackbars", 0, 255, nothing )

h_h = cv2.createTrackbar("h-h","trackbars", 179, 179, nothing )
h_s = cv2.createTrackbar("h-s","trackbars", 255, 255, nothing )
h_v = cv2.createTrackbar("h-v","trackbars", 255, 255, nothing )


while True:
    
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #blur = cv2.GaussianBlur(hsv, (5,5), 0)
    
    lh = cv2.getTrackbarPos("l-h", "trackbars")
    ls = cv2.getTrackbarPos("l-s", "trackbars")
    lv = cv2.getTrackbarPos("l-v", "trackbars")
    
    hh = cv2.getTrackbarPos("h-h", "trackbars")
    hs = cv2.getTrackbarPos("h-s", "trackbars")
    hv = cv2.getTrackbarPos("h-v", "trackbars")
    
    # pick the limits of the obj in the color frame
    lower_gray = np.array([lh,ls,lv])
    upper_gray = np.array([hh,hs,hv])
    # create a mask
    mask = cv2.inRange(hsv, lower_gray, upper_gray)
    
    show = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.imshow("colour alone", show)
    cv2.imshow("mask", mask)
    
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
        
cap.release()
cv2.destroyAllWindows()
    