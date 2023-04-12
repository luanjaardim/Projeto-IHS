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
        self.targetList, hierarquias = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contorno in self.targetList:
            x,y,w,h = cv2.boundingRect(contorno)
            print(x,y)
            # cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            # cv2.putText(img, 'X: %d  y: %d' % (x, y), (x,y+h+14), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    
    def adjust(self):
        pass