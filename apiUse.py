import cv2
import numpy as np
from torreta_lib import *
import serial
import time

torreta = IO()

# Open a serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

# Initialize webcam
cap = cv2.VideoCapture(0)

spinFlag = False
shootFlag = False
ligaLeds = 0x3FFFF
estado = 1

def shooting():
    if torreta.get_SW(0) == 1:
        contagem = 0x3FFFF
        display = 5
        for i in range(36):
            if(i % 7) == 0:
                count = '000' + str(display)
                torreta.put_DP(0, count)
                print("Tiro em:", display)
                display -= 1
            if (i % 2) == 0:
                time.sleep(278 / 1000)
                torreta.put_LD(contagem >> i//2)
        print('POW')
        torreta.put_DP(0, "0000")
        ser.write(b's')
    else:
        print('No POW')

while torreta.get_SW(16) == 1:
    
    sendChar = 0

    # 0 para manual e 1 para automatic
    if torreta.get_SW(17) == 0 :
        print('modo manual!')
        
        # controla o giro da base
        if (torreta.get_PB(1) == 0 and torreta.get_PB(0) == 1):
            # Gira para esquerda
            print('Girando pra esquerda!')
            ser.write(b'e')
        elif (torreta.get_PB(1) == 1 and torreta.get_PB(0) == 0):
            # Gira para direita
            print('Girando pra direita!')
            ser.write(b'd')

        else:
            print('sem giro')

        # controla a inclinacao do tiro
        if (torreta.get_PB(3) == 0 and torreta.get_PB(2) == 1 ):
            # Inclina pra cima
            print('inclinando para cima!')
            ser.write(b'c')
        elif (torreta.get_PB(3) == 1 and torreta.get_PB(2) == 0 ):
            # Inclina pra baixo
            print('inclinando para baixo!')
            ser.write(b'b')
        else:
            print('sem inclinacao')

        # liga os motores
        if torreta.get_SW(1) == 1 and  spinFlag == False:
            print('motores rodando')
            spinFlag = True
            ser.write(b'O')
        elif spinFlag == True and torreta.get_SW(1) == 0:
            print('motores parados')
            spinFlag = False
            ser.write(b'o')
    
        # atira
        if torreta.get_SW(0) == 1 and shootFlag == False:
            print('POW')
            shootFlag = True
            shooting()
            ser.write(b's')
        elif torreta.get_SW(0) == 0:
            shootFlag = False
            print('No POW')


        if spinFlag == True:
            torreta.put_LD(ligaLeds if  estado == 1 else 0x0)
            estado = 1 if estado == 0 else 0
        else:
            torreta.put_LD(0x0)

        time.sleep(0.1)

    else:
        print('modo auto!')

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert BGR to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range of blue color in HSV
        lower_blue = np.array([62,158,38])
        upper_blue = np.array([64,214,255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Apply the mask to the original frame
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # calculos
        axes = (30,30)
        center = (int(frame.shape[1]/2), int(frame.shape[0]/2)+100)
        cv2.ellipse(frame, center, axes, 0, 0, 360, (0,255,0), 1)
        targetList, hierarquias = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contorno in targetList:
                if cv2.contourArea(contorno) > 250:
                    objCenter, radius = cv2.minEnclosingCircle(contorno)
                    # Check if the pixel is inside the ellipse
                    if (((objCenter[0] - center[0]) / axes[0]) ** 2 + ((objCenter[1] - center[1]) / axes[1]) ** 2) <= 1:
                        print("Objeto no range!")
                    else:
                        print("Objeto fora do range!")
                        distance_x = objCenter[0] - center[0]
                        distance_y = center[1] - objCenter[1] 
                        if(distance_x < 0):
                            #girar para esquerda
                            ser.write(b'e')
                        else:
                            #girar para direita
                            ser.write(b'd')
                        if(distance_y < 0):
                            #inclinar para baixo
                            ser.write(b'b')
                        else:
                            #inclinar para cima
                            ser.write(b'c')# 

        cv2.waitKey(1)

        # liga os motores
        if torreta.get_SW(1) == 1 and  spinFlag == False:
            print('motores rodando')
            spinFlag = True
            ser.write(b'O')
        elif spinFlag == True and torreta.get_SW(1) == 0:
            print('motores parados')
            spinFlag = False
            ser.write(b'o')
    
        # atira
        if torreta.get_SW(0) == 1 and shootFlag == False:
            print('POW')
            shootFlag = True
            shooting()
            ser.write(b's')
        elif torreta.get_SW(0) == 0:
            shootFlag = False
            print('No POW')


        if spinFlag == True:
            torreta.put_LD(ligaLeds if  estado == 1 else 0x0)
            estado = 1 if estado == 0 else 0
        else:
            torreta.put_LD(0x0)

        # Display the resulting frame
        cv2.imshow('Mascara',result)
        cv2.imshow('Preview', frame)