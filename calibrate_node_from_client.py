import cv2 as cv
import logging
import numpy as np
import yaml

from client import StreamerRx

if __name__=='__main__':
    
    logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)
    logging.debug("Opening stream")

    # addr = ('raspberrypi.local',8000)
    # fname = "camcal.yaml"

    addr = ('10.0.11.2',8000)
    fname = "deepi1.yaml"

    with StreamerRx(addr, rotation=None, calibration=None) as stream:

        stream.start()
        
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.    

        while True:
        
            img = stream.frame
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            
            ret, corners = cv.findChessboardCorners(gray, (7,6), None)
            
            if ret == True:
                logging.debug("Found chessboard")
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11,11),
                                           (-1,-1), criteria)
                imgpoints.append(corners2)
                
                cv.drawChessboardCorners(img, (7,6), corners2, ret)

            cv.imshow('img', img)
            k = cv.waitKey(1)
            
            if k==27:
                # close out on escape
                break
        
        logging.info("Closing windows")
        cv.destroyAllWindows()
        cv.waitKey(1)

    logging.info("Running calibration")
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints,
                                                      imgpoints,
                                                      gray.shape[::-1],
                                                      None, None)

    print("ret")
    print(ret)
    
    print("Camera Matrix")
    print(mtx)

    print("Distortion Coefficient")
    print(dist)

    

    logging.info("Optimizing camera matrix")
    h,  w = img.shape[:2]
    camera_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    # undistort
    dst = cv.undistort(img, mtx, dist, None, camera_matrix)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imshow('undistort', dst)    

    print("Camera Matrix")
    print(camera_matrix)
    print(roi)

    print("Remapping")
    mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None,
                                            camera_matrix, (w,h), 5)

    dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imshow('remap', dst)
    cv.imshow('orig',img)

    data = {"camera_matrix":mtx.tolist() , "dist_coeff":dist.tolist()}
    with open(fname, 'w') as f:
        yaml.dump(data,f)

    cv.waitKey(0)
        
