import cv2

class Tracker:
    def __init__(self):

        #aim parameters
        self.axes = (100,50)

        #color segmentation parameters
        self.minThresh = (0,0,0)
        self.maxThresh = (180, 255, 255)
        
        #targets position list
        self.targetList = []

    #update detecting color parameters
    def update_HSV_thresh(self, min, max):
        self.minThresh = min
        self.maxThresh = max
        return True

    def detect(self, mask, frame):

        center = (int(frame.shape[1]/2), int(frame.shape[0]/2))

        self.targetList, hierarquias = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contorno in self.targetList:
            if cv2.contourArea(contorno) > 250: 
                objCenter, radius = cv2.minEnclosingCircle(contorno)
                # Check if the pixel is inside the ellipse
                if (((objCenter[0] - center[0]) / self.axes[0]) ** 2 + ((objCenter[1] - center[1]) / self.axes[1]) ** 2) <= 1:
                    print("Objeto no range!")
                else:
                    self.adjust(center[0]-objCenter[0], center[1]-objCenter[1])

        #draw elipse on frame
        cv2.ellipse(frame, center, self.axes, 0, 0, 360, (0,255,0), 1)


        return frame

    def adjust(self, x, y):
        x = min(max(x, 0), 1)
        y = min(max(y, 0), 1)
        print(x, y)