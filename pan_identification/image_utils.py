"""
    File name           : pan_identification
    Author              : siddhi.bajracharya
    Date created        : 2/3/2021
    Date last modified  : 2/3/2021
    Python Version      : 3.6.5
    Description         : Various utilities for image processing.
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def plot_image(image):
    """
    Plots an image.
    :param image: image to plot
    :return:
    """
    plt.rcParams['figure.figsize'] = 20, 20
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def read_image(path):
    """
    Read image from file.
    :param path: File path
    :return: cv2 image.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image file at {path} not found.")
    return cv2.imread(path)


def resize(image, resize_shape):
    """
    Resizes the image.
    :param image: Image to resize.
    :param resize_shape: Shape of image after resize.
    :return:
    """
    return cv2.resize(image, resize_shape)


def sharpen_image(image):
    """
    Sharpens the image.
    :param image: Image to sharpen.
    :return: sharpened image.
    """

    # this specific filter is for sharpening
    kernel = np.array([[-1,-1,-1], [-1, 9,-1],[-1,-1,-1]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened


def normalize_image(image):
    """
    Normalizes image.
    :param image: Image to normalize.
    :return: normalized image.
    """
    rgb_planes = cv2.split(image)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
    result_norm = cv2.merge(result_norm_planes)

    return result_norm


def crop(image, *dim):
    """
    Crops image
    :param image: image to crop.
    :param dim: Dimensions of the cropped image. (x,y,w,h)
    :return: cropped image.
    """
    return image[dim[1]:dim[1] + dim[3], dim[0]:dim[0] + dim[2]]


def rem_lines(image):
    """
    Removes lines from image.
    :param image: Image from which lines are to be removed.
    :return: Image with lines removed.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # close lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 1))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=2)

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    contours = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for c in contours:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 3)

    # Vertical horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=3)
    contours = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for c in contours:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 10)
    return image


def preprocess_for_tesseracts(image):
    """
    Preprocessing step for pytesseract.
    :param image: Image to preprocess
    :return: preprocessed image.
    """
    result_norm = normalize_image(image)
    img = cv2.cvtColor(result_norm, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    return blur

