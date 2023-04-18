from torreta_lib impot *
import time
import serial

torreta = IO()

# Define the 6 bits to send
bits = [0, 0, 0, 0, 0, 0]

# Open a serial connection to the Arduino
ser = serial.Serial('COM3', 9600)

while True:
    
    # 0 para manual e 1 para automatico
    if torreta.read_sw(17) == 0 :
        print('modo manual!')

        # controla o giro da base
        if (torreta.get_pb(1) == 0 and torreta.get_pb(0) == 1):
            # Gira para direita
            print('Girando pra direita!')
            bits[0] = 0
            bits[1] = 1
        elif (torreta.get_pb(1) == 1 and torreta.get_pb(0) == 0):
            # Gira para esquerda
            print('Girando pra esquerda!')
            bits[0] = 1
            bits[1] = 0
            
        # controla a inclinacao do tiro
        if (torreta.get_pb(3) == 0 and torreta.get_pb(2) == 1 ):
            # Inclina pra cima
            print('inclinando para cima!')
            bits[2] = 0
            bits[3] = 1
        elif (torreta.get_pb(3) == 0 and torreta.get_pb(2) == 1 ):
            # Inclina pra baixo
            print('inclinando para baixo!')
            bits[2] = 1
            bits[3] = 0

        # liga os motores
        if torreta.get_sw(1) == 1:
            print('motores rodando')
            bits[4] = 1
        else:
            print('motores parados')
            bits[4] = 0
    
        # atira
        if torreta.get_sw(0) == 1:
            start_time = time.time()
            elapsed_time = 0
            while elapsed_time < 5:
                time.sleep(0.1)
                elapsed_time = time.time() - start_time
            print('POW')
            bits[5] = 1
        else:
            print('No POW')
            bits[5] = 0

        # Convert the bits to a single byte
        byte_value = 0
        for bit in bits:
            byte_value = (byte_value << 1) | bit
        # Send the byte to the Arduino
        ser.write(bytes([byte_value]))

    else:
        print('modo auto!')