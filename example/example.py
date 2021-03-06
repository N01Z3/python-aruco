'''
Created on 05.04.2016

@author: fehlfarbe
'''
import cv2
import numpy as np
import aruco

if __name__ == '__main__':
    
    # load board and camera parameters
    boardconfig = aruco.BoardConfiguration("chessboardinfo_small_meters.yml")
    camparam = aruco.CameraParameters()
    camparam.readFromXMLFile("dfk72_6mm_param2.yml")
    
    # create detector and set parameters
    detector = aruco.BoardDetector()
    detector.setParams(boardconfig, camparam)
    # set minimum marker size for detection
    markerdetector = detector.getMarkerDetector()
    markerdetector.setMinMaxSize(0.01)
    
    # load video
    cap = cv2.VideoCapture("example.mp4")
    ret, frame = cap.read()
    
    if not ret:
        print "can't open video!"
        exit(-1)
    
    while ret:
        likelihood = detector.detect_mat(frame)
        
        markers = markerdetector.detect(frame, camparam)
        
        if likelihood > 0.1:
            # get board and draw it    
            board = detector.getDetectedBoard()
            board.draw(frame, np.array([255, 255, 255]), 2)

            print "detected ids: ", ", ".join(str(m.id) for m in board)
            
        # show frame
        cv2.imshow("frame", frame)
        cv2.waitKey(100)
        
        # read next frame
        ret, frame = cap.read()
        