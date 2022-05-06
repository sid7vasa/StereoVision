import cv2
import numpy as np
import glob
from tqdm import tqdm
from matplotlib import pyplot as plt
import cv2 as cv


def main():
    H1 = np.load("../notebooks/H1.npy")
    H2 = np.load("../notebooks/H2.npy")

    cap = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(3)

    if not cap.isOpened() or not cap2.isOpened():
        print("Cannot open camera")
        exit()

    count = 0
    block_size = 11
    min_disp = -128
    max_disp = 128
    uniquenessRatio = 5
    speckleWindowSize = 200
    speckleRange = 2
    disp12MaxDiff = 0

    while True:
        # Capture frame-by-frame
        ret, img1 = cap.read()
        ret2, img2 = cap2.read()
        h1, w1 = img1.shape[:2]
        h2, w2 = img1.shape[:2]

        img1_rectified = cv.warpPerspective(img1, H1, (w1, h1))
        img2_rectified = cv.warpPerspective(img2, H2, (w2, h2))

        num_disp = max_disp - min_disp

        stereo = cv.StereoSGBM_create(
            minDisparity=min_disp,
            numDisparities=num_disp,
            blockSize=block_size,
            uniquenessRatio=uniquenessRatio,
            speckleWindowSize=speckleWindowSize,
            speckleRange=speckleRange,
            disp12MaxDiff=disp12MaxDiff,
            P1=8 * 1 * block_size * block_size,
            P2=32 * 1 * block_size * block_size,
        )
        disparity_SGBM = stereo.compute(img1_rectified, img2_rectified)

        # Normalize the values to a range from 0..255 for a grayscale image
        disparity_SGBM = cv.normalize(disparity_SGBM, disparity_SGBM, alpha=255,
                                      beta=0, norm_type=cv.NORM_MINMAX)
        disparity_SGBM = np.uint8(disparity_SGBM)

        # Display the resulting frame
        cv2.imshow('Disparity', disparity_SGBM)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('s'):
            print("Saving image")
            cv2.imwrite("./testData/" + str(count) + "L.jpg", img1)
            cv2.imwrite("./testData/" + str(count) + "R.jpg", img2)
            count = count + 1
    # When everything done, release the capture
    cap.release()
    cap2.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
