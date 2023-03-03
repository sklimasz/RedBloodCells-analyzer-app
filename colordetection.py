import cv2
import numpy as np
from collections import Counter

class BackgroundColorDetector():    # estimation of rgb value of background
    def __init__(self, image):
        self.img = image.copy()
        self.manual_count = {}
        self.w, self.h, self.channels = self.img.shape
        self.total_pixels = self.w*self.h


    def count(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.img[x, y, 2], self.img[x, y, 1], self.img[x, y, 0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1

    def average_colour(self):
        red = 0
        green = 0
        blue = 0
        sample = 10
        for top in range(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]

        average_red = int(red / sample)
        average_green = int(green / sample)
        average_blue = int(blue / sample)
        return([average_red,average_green,average_blue])

    def detect(self):
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)
        # self.percentage_of_first = (
        #     float(self.number_counter[0][1])/self.total_pixels)
        # if self.percentage_of_first > 0.5:
        #     return(self.number_counter[0][0])
        # else:
        return(self.average_colour())
