import cv2

class Tracker:
    def __init__(self):

        #aim parameters
        self.horizontalMargin = 100
        self.verticalMargin = 100

        #color segmentation parameters
        self.minThresh = (0,0,0)
        self.maxThresh = (180, 255, 255)
        
        #targets position list
        self.targetList = []

        self.adjust()

    #update detecting color parameters
    def update_HSV_thresh(self, min, max):
        self.minThresh = min
        self.maxThresh = max
        return True

    def detect(self, mask):
        pass
    
    def ajdust():
        pass