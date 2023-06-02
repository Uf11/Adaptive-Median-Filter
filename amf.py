# You are required to implement Adaptive Median Filter  using appropriate GUI. You will input an image and then add
# salt & Pepper noise of increasing probability and then applying the above filter accordingly.
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import numpy as np
import cv2
import random
import sys


class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(".\\main_window.ui", self)
        self.img = None
        self.Select_Button = self.findChild(QPushButton, "Select_Button")
        self.label = self.findChild(QLabel, "label")
        self.Filter_Button = self.findChild(QPushButton, "Filter_Button")
        self.pixmap = None
        self.Select_Button.clicked.connect(self.file_selector)
        self.Filter_Button.clicked.connect(self.noise_window)
        self.show()

    def file_selector(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "c:",
                                                "All Files (*);;Bmp Files (*.bmp);;Jpg Files (*.jpg)")
        if file_name:
            self.pixmap = QPixmap(file_name[0])
            self.label.setPixmap(self.pixmap)
            self.img = cv2.imread(file_name[0])

    def noise_window(self):
        if self.img is None:
            return
        window = Noise(self.img)
        window.exec_()


class Noise(QDialog):
    def __init__(self, img):
        super(Noise, self).__init__()
        uic.loadUi(".\\noise_window.ui", self)
        self.img = img
        self.Adaptive_Median_Filter_Button = self.findChild(QPushButton, "Adaptive_Median_Filter_Button")
        self.Adaptive_Median_Filter_Button.clicked.connect(self.calculate)
        self.noise_val_text = self.findChild(QLineEdit, "Noise_val")
        self.show()

    def calculate(self):
        noise_val = float(self.noise_val_text.text())
        cv2.imshow('original', self.img)
        noisy_img = add_salt_pepper_noise(self.img, noise_val)
        cv2.imshow('noisy', noisy_img)
        if len(self.img.shape) == 3:
            filtered_img = for_color_image(noisy_img)
        else:
            filtered_img = adaptive_median_filter(noisy_img)
        cv2.imshow('filtered', filtered_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def add_salt_pepper_noise(img, prob):
    output = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            rand = np.random.random()
            if rand <= prob:
                rand = random.choice([0, 255])
                output[i][j] = rand
            else:
                output[i][j] = img[i][j]
    return output


def add_pad(img, pad):
    # 2D array of zeros , 2*pad is the size for opposite sides
    output = np.zeros((img.shape[0] + 2 * pad, img.shape[1] + 2 * pad))
    output[pad:img.shape[0] + pad, pad:img.shape[1] + pad] = img
    return output


def calc_value(img, pix, window_size, max_window_size, pad):
    while True:
        window = img[pix[0] + pad:pix[0] + window_size + pad, pix[1] + pad:pix[1] + window_size + pad]
        window = window.flatten()
        sorted_window = np.sort(window)
        g_min = sorted_window[0]
        g_max = sorted_window[-1]
        g_med = np.median(sorted_window)
        if g_min < g_med < g_max:
            if g_min < img[pix[0]][pix[1]] < g_max:
                return img[pix[0]][pix[1]]
            return g_med
        window_size += 2
        if window_size > max_window_size:
            return img[pix[0]][pix[1]]


def adaptive_median_filter(img):
    output = np.zeros_like(img)
    initial_window_size = 3
    max_window_size = 11
    pad = max_window_size // 2
    h, w = img.shape
    img = add_pad(img, pad)
    print(img.shape)
    for i in range(h):
        for j in range(w):
            output[i][j] = calc_value(img, [i, j], initial_window_size, max_window_size, pad)
    return output


def for_color_image(img):
    h, w, c = img.shape
    output = np.zeros_like(img)
    for i in range(c):
        output[:, :, i] = adaptive_median_filter(img[:, :, i])
    return output


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Main()
    app.exec_()
