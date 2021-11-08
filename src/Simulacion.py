import statistics
import pandas as pd
import random as rd


#import scipy as sc
#from scipy.stats import gamma
from Funciones import *


# Variables importantes de la simulacion
SIMULATION_RUNS = 1000
SIMULATION_HOURS = 10
WAIT_THRESHOLD = 6 / 60
REJECTED_JOBS = 0


RUN_DATAFRAMES = []


for i in range(SIMULATION_RUNS):
    # El array de servidores contiene el tiempo en que se realizo
    # la ejecucion final de cada uno, se explica más
    # adelante en el comentario de TEORIA
    servers_last_finished_times = [0, 0, 0, 0]
    last_arrival_time = 0
    interarrival_time = interarrival_times(SIMULATION_HOURS, 30)

    interarrival_times_list = []
    arrival_times_list = []
    wait_times_list = []
    service_times_list = []
    finish_times_list = []
    start_times_list = []
    system_times_list = []


    # Loop de simulacion
    for interarrival in interarrival_time:

        # Calculo de los tiempos de llegada a partir de
        # los tiempos entre arrivos
        arrival_time = interarrival + last_arrival_time
        last_arrival_time = arrival_time

        '''
        Idea:

        Iteracion 1:
        Usar un array con tiempos finales,
        asignar proceso a servidor con tiempo final mas bajo.

        Iteracion 2:
        Intentar implementar un threshold para 
        poder sacar los jobs que tarden mas de 6 minutos
        '''
        # TEORIA:
        # El servidor con tiempo mas pequeño
        # Va a estar vacio o será el proximo
        # En desocuparse

        min_index = servers_last_finished_times.index(min(servers_last_finished_times))

        #Revision de que el tiempo de espera no sea superior al threshold
        if servers_last_finished_times[min_index] - arrival_time <= WAIT_THRESHOLD:

            # Entonces, esto deberá bastar para seleccionar el servidor
            if arrival_time > servers_last_finished_times[min_index]:
                init_time = arrival_time
            else:
                init_time = servers_last_finished_times[min_index]

            # Ahora, es necesario elegir una funcion
            # Que nos genere los valores para
            # Tiempo de servicio de acuerdo al servidor
            wait_time = init_time - arrival_time

            service_time = service_time_fromID(min_index)

            final_time = init_time + service_time

            # Ajuste del tiempo final en el servidor
            # que fue utilizado para la ejecucion actual
            servers_last_finished_times[min_index] = final_time
            # Ajuste al tiempo global - ERROR QUE ESTOY HACIENDO??
            # ESTE ES EL TIEMPO EN EL SISTEMA NO EL GLOBAL
            system_time = final_time - arrival_time

            # Recoleccion de datos para estadisticas
            interarrival_times_list.append(interarrival)
            arrival_times_list.append(arrival_time)
            wait_times_list.append(wait_time)
            service_times_list.append(service_time)
            finish_times_list.append(final_time)
            start_times_list.append(init_time)
            system_times_list.append(system_time)

        else:
            REJECTED_JOBS += 1

    df = pd.DataFrame(data={
        'Interarrival': interarrival_times_list, 'Arrival Time': arrival_times_list, 'Initial Service Time': start_times_list, 'Wait Time': wait_times_list, 'Service Time': service_times_list, 'Final Time': finish_times_list, 'System Time': system_times_list
    })

    RUN_DATAFRAMES.append(df)

ndf = RUN_DATAFRAMES[0]

for d in RUN_DATAFRAMES[1:-1]:
    ndf = ndf.append(d, ignore_index = True)


ndf.to_csv(r'Dataframes.csv')