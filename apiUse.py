from torreta_lib impot *
import time

torreta = IO()

while True:
    
    # 0 para manual e 1 para automatico
    if torreta.read_sw(17) == 0 :
        print('modo manual!')

        # controla o giro da base
        if (torreta.get_pb(1) == 0 and torreta.get_pb(0) == 1):
            # Gira para direita
            print('Girando pra direita!')
        elif (torreta.get_pb(1) == 1 and torreta.get_pb(0) == 0):
            # Gira para esquerda
            print('Girando pra esquerda!')
        
        # controla a inclinacao do tiro
        if (torreta.get_pb(3) == 0 and torreta.get_pb(2) == 1 ):
            # Inclina pra cima
            print('inclinando para cima!')
        elif (torreta.get_pb(3) == 0 and torreta.get_pb(2) == 1 ):
            # Inclina pra baixo
            print('inclinando para baixo!')

        # liga os motores
        if torreta.get_sw(1) == 1:
            print('motores rodando')
        else:
            print('motores parados')

        # atira
        if torreta.get_sw(0) == 1:
            start_time = time.time()
            elapsed_time = 0
            while elapsed_time < 5:
                time.sleep(0.1)
                elapsed_time = time.time() - start_time
            print('POW')
        else:
            print('No POW')

    else:
        print('modo auto!')