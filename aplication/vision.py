import cv2
import numpy as np

class Vision:
    def __init__(self, cameraSource=0):
        self.cam = cv2.VideoCapture(cameraSource)
        self.minPoint = (0,0) # Inicializando valor por que deu problema
        self.maxPoint = (0,0)

        self.__updateFrame()

    def __updateFrame(self): #essa funcao atualiza o frame, vai ser usada quando chegar na observationPose do robo
        ret, frame = self.cam.read()
        while ret == False:
            ret, frame = self.cam.read()
        self.frame = cv2.resize(frame, (453, 340))

    def getFrame(self):
        self.__updateFrame()
        return self.frame