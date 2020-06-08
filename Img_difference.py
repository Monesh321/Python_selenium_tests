import time

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


# from selenium import webdriver


# from skimage.measure import compare_ssim as ssim

# def screenCapture(driver, url, screenshotName_prefix):
#     driver.get(url)
#     time.sleep(10)
#     driver.save_screenshot(screenshotName_prefix + driver.title.replace(' ', '_') + ".png")
#     time.sleep(2)
#     driver.close()


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])


# return the MSE, the lower the error, the more "similar"
# the two images are
# def diff_remove_bg(img0, img, img1):
#     d1 = diff(img0, img)
#     d2 = diff(img, img1)
#     return cv2.bitwise_and(d1, d2)

def Img_Comparison(img1, img2, filename):
    x1 = cv2.imread(img1)
    x2 = cv2.imread(img2)
    x1 = cv2.cvtColor(x1, cv2.COLOR_BGR2GRAY)
    x2 = cv2.cvtColor(x2, cv2.COLOR_BGR2GRAY)

    absdiff = cv2.absdiff(x1, x2)
    cv2.imwrite(filename + "_absolute.png", absdiff)

    diff = cv2.subtract(x1, x2)
    result = not np.any(diff)

    m = mse(x1, x2)
    s = ssim(x1, x2, multichannel=True)

    print("mse: %s, ssim: %s" % (m, s * 100))

    if result:
        print("The images are the same")
    else:
        cv2.imwrite(filename + "_relative.png", diff)
        print(diff)
        print("The images are different")

# Img_Comparison("SCREENSHOTS/after_build_Sun_Life_|_Life_Insurance_Investments_&_Group_Benefits_0.png",
#                "SCREENSHOTS/after_build_Life_moments_|_Sun_Life_1.png")
