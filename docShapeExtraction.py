import os
import sys
import numpy as np
import cv2


def main():
    cap = cv2.VideoCapture(0)

    if (cap.isOpened()):
        bgs = cv2.createBackgroundSubtractorMOG2(history = 80)

        while True:
            ret, frame = cap.read()
            kernel = np.ones((11,11),np.uint8)

            # if video capture error
            if ret == False:
                break

            fgMask = bgs.apply(frame)
            paperMask = cv2.bitwise_and(frame, frame, mask = fgMask)
            # convert frame to gray grayScale
            gray = cv2.cvtColor(paperMask, cv2.COLOR_BGR2GRAY)

            # gaussian blur to smooth out edges
            paperBlur = cv2.GaussianBlur(gray, (41,41), 0)
            dilation = cv2.dilate(paperBlur, kernel, iterations = 1)


            # thresh hold to create binary img from gray grayScale
            threshold = 20
            ret, paper = cv2.threshold(dilation, threshold, 255, cv2.THRESH_BINARY)
            im2, contours, hierarchy = cv2.findContours(paper,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, contours, -1, (0,255,0), 3)


            cv2.imshow('img', frame)

            if(cv2.waitKey(5) & 0xFF == ord('q')):
                break

        cv2.destroyAllWindows()
        cap.release()



main()
