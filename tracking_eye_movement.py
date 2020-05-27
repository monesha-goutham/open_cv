import cv2
import numpy as np
import imutils

# reading a video file with eye movement
cap = cv2.VideoCapture("videos\\eye_recording.flv")
# codec for recording
codec = cv2.VideoWriter_fourcc(*"XVID")
# define writer
writer = cv2.VideoWriter("videos\\tracked_eye_movement.avi", codec, 30, (int(cap.get(3)),int(cap.get(4))))

while True:
    
    ret, frame = cap.read()
    if ret is False:
        break
        
    # create an ROI by cropping out uncessary portions of video
    # coords obtained by photoshop
    roi = frame[269: 795, 650: 1416]
    # roi's dimensions
    (img_height, img_width) = roi.shape[:2]
    # print(roi.shape)
    
    # we dont need color for this task
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # lets include some blur for reducing noise in mask
    blur = cv2.GaussianBlur(gray_roi, (7, 7), 0)
    
    # let's track the pupil (pitch black)
    # using threshold to track
    _, mask = cv2.threshold(blur, 3, 255, cv2.THRESH_BINARY_INV)

    # the mask created is perfect, we draw contours and detect the eyemoment using contour area
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # lets draw contours only on contours with largest area
    # so we sort the contours area-wise in descending order
    con_areas = sorted(contours, key = lambda x: cv2.contourArea(x), reverse = True)
    
    # draw the largest (1st contour) alone
    for conts in con_areas:
        # cv2.drawContours(roi, conts, -1, (0, 255, 0), thickness= 4 )
        
        # lets draw a circle around the contour area instead of contour
        (x, y, w, h) = cv2.boundingRect(conts)
        center_x = int(x + w //2)
        center_y = int(y + h // 2)
        cv2.circle(roi, (center_x, center_y), radius = (w+h)//4, color = (0, 0, 255), thickness = 3 )
        
        # lets draw some coordinate lines to give a better estimate of eye movement
        cv2.line(roi, (center_x, 0), (center_x, img_height), color = (0, 255, 255), thickness = 1)
        cv2.line(roi, (0, center_y), (img_width, center_y), color = (0, 255, 255), thickness = 1)

        # just the largest needed, so break after 1st iteration
        break
        
    
    cv2.imshow("mask", mask)
    cv2.imshow("gray_roi", gray_roi)
    cv2.imshow("roi", roi)
    writer.write(roi)

    
    # wait time 30 ms to slow down the video
    key = cv2.waitKey(30)
    if key == ord("q"):
        break

        
# cap.release()
writer.release()
cv2.destroyAllWindows()