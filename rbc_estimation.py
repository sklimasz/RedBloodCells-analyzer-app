import cv2
import numpy as np
import colordetection as cd

class RBC_analyzer:
    def __init__(self, imagePath, background, threshold = 0.1, erodeIterations = 1, AreaOfOneCell = 2000,):
        self.imagePath   = imagePath
        self.image       = cv2.imread(imagePath, 1)
        self.imageOG     = self.image.copy()
        self.imageToShow = self.image.copy()

        self.background = background
        self.erodeIterations = erodeIterations
        self.thresholdBackground = threshold
        self.RBC_count   = 0
        self.contours    = [ [] , [] , [] , [] ]
        
        self.imagesEachStep = [] # contains transitional images

        self.AreaOfOneCell = AreaOfOneCell
        self.erodeIterations = erodeIterations

    def removeWhiteBloodCells(self): # remove purple white blood cells from image
        imageTemporaryHSV = self.imageOG.copy()
        imageTemporaryHSV = cv2.cvtColor(imageTemporaryHSV, cv2.COLOR_BGR2HSV)
        # convert image to HSV
        # HSV is more handy than RGB in this scenario

        lowerPurple = np.array([30, 60, 0])
        upperPurple = np.array([255, 255, 255])
        # range of blue and purple in HSV

        mask = cv2.inRange(imageTemporaryHSV, lowerPurple, upperPurple)
        # get all pixels that match given color range

        self.image[mask>0] = [255, 255, 255]
        # change all those pixels to pure-white
    
    def removeBackground(self): # remove background - change it to pure white

        background_Grayscale = int ( 0.2989 * self.background[0] + 0.5870 * self.background[1] + 0.1140 * self.background[2] )
        upperThreshold = (1+self.thresholdBackground) * background_Grayscale
        lowerThreshold = (1-self.thresholdBackground) * background_Grayscale
        # threshholds can be changed
        # but it might lead to some RBC being removed
        # or some background not being removed

        imageTemporaryGray = self.imageOG.copy()
        imageTemporaryGray = cv2.cvtColor(imageTemporaryGray, cv2.COLOR_BGR2GRAY)
        # convert image to grayscale
        
        mask = cv2.inRange(imageTemporaryGray, lowerThreshold, upperThreshold)
        # get all pixels that match background color with some deviation

        self.image[mask>0] = [255, 255, 255]
        # change all those pixels to pure-white

    def analyze_rbc(self):
        self.imagesEachStep.append(self.imageOG)
        self.removeWhiteBloodCells()
        self.imagesEachStep.append(self.image.copy())

        self.removeBackground()
        self.imagesEachStep.append(self.image.copy())

        imageGrey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.imagesEachStep.append(imageGrey)

        imageInverted = cv2.bitwise_not(imageGrey)
        self.imagesEachStep.append(imageInverted)
        # change image to greyscale, invert colors (background is now black)
        # its helpful in erosion
        

        kernel = np.ones((2, 2), np.uint8)
        imageEroded = cv2.erode(imageInverted, kernel, iterations = self.erodeIterations)
        self.imagesEachStep.append(imageEroded)
        # erode the image in order to get rid of thin lines
        # that are leftovers from purple white bloods cells
        # these thin lines would lead to incorrect contouring
        # more iterations get rid of thicker lines,
        # but might lead to some RBC not being counted
        # eroding might also separate clustered cells

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        imageMorphed = cv2.morphologyEx(imageEroded, cv2.MORPH_OPEN, kernel) 
        contours, _ = cv2.findContours(imageMorphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.imagesEachStep.append(imageMorphed)
        # get rid of lines using morphology (similiar to erosion),
        # then find contours

        for contour in contours:
            if cv2.contourArea(contour) > 50*self.AreaOfOneCell:
                self.contours[3].append(contour)
                self.RBC_count += 20
    
            elif cv2.contourArea(contour) > 6*self.AreaOfOneCell:
                self.contours[2].append(contour)
                self.RBC_count += 5

            elif cv2.contourArea(contour) > 3*self.AreaOfOneCell:
                self.contours[1].append(contour)
                self.RBC_count += 2.5

            elif cv2.contourArea(contour) > self.AreaOfOneCell:
                self.contours[0].append(contour)
                self.RBC_count += 1
        # analyze the contours, approximate how many cells are in each
        # get rid of very small false contours that dont contain red blood cells
        # correct logic of contour area and RBC count may vary
        # depending on the database e.g. resolution of image
        # change self.AreaOfOneCell, see what matches images from database

        cv2.drawContours(self.imageToShow, self.contours[0], -1, (0, 0, 255)    , 3)
        cv2.drawContours(self.imageToShow, self.contours[1], -1, (0, 255, 0)    , 3)
        cv2.drawContours(self.imageToShow, self.contours[2], -1, (0, 255, 255)  , 3)
        cv2.drawContours(self.imageToShow, self.contours[3], -1, (255, 102, 255), 3)
        # draw the contours onto the original image
        # different colors correspond to number of cells in a contour

        self.imagesEachStep.append(self.imageToShow)

        return [self.imagesEachStep, self.RBC_count]


