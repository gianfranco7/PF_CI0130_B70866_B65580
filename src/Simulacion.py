import statistics
from typing import final
import pandas as pd
import random as rd


#import scipy as sc
#from scipy.stats import gamma
from Funciones import *


#Variables importantes de la simulacion
OPENING_TIME = 0
SIMULATION_HOURS = 10
GLOBAL_TIME = OPENING_TIME
WAIT_TRESHOLD = 6
REJECTED_JOBS = 0


#Internal Simulation Variables
client_queue = []


#Tuplas en formato Id, Ocupado, Tiempo de servicio
servers = [0, 0, 0, 0]
last_final_time = 0
last_arrival_time = 0
interarrival_time = interarrival_times(SIMULATION_HOURS, 30)

interarrival_times_list = []
arrival_times_list = []
wait_times_list = []
service_times_list = []
finish_times_list = []
start_times_list = []
global_times_list = []


# Loop de simulacion
for interarrival in interarrival_time:

    arrival_time = interarrival + last_arrival_time
    last_arrival_time = arrival_time    
    

    #Cambiar a multiservidor
    if arrival_time > last_final_time:    #Cajero desocupado
        init_time = arrival_time
    else:
        init_time = last_final_time

    wait_time = init_time - arrival_time

    service_time = rd.uniform(3, 5)

    final_time = init_time + service_time
    #Fin de cambio a multiservidor


    GLOBAL_TIME += final_time - arrival_time

    

    interarrival_times_list.append(interarrival)
    arrival_times_list.append(arrival_time)
    wait_times_list.append(wait_time)
    service_times_list.append(service_time)
    finish_times_list.append(final_time)
    start_times_list.append(init_time)
    global_times_list.append(GLOBAL_TIME / 60)



df = pd.DataFrame(data={
'Interarrival': interarrival_times_list, 'Arrival time': arrival_times_list, 'Initial service time': start_times_list ,'Wait time': wait_times_list, 'Service time' : service_times_list, 'Final time': finish_times_list, 'Global time' : global_times_list
})




    
print(df)

print(sum(df['Interarrival']))
print(statistics.mean(df['Interarrival']))
print(max(df['Global time']))

#Parametros a calcular
#Expected response time
#Expected waiting time for random job
#Expected length of queue - jobs in service currently
#Maximum waiting time 10 hrday
# waiting_queue = []
#print("Maximum waiting time:", max(waiting_queue))
#Minimum waiting time 10 hrday
#print("Minimum waiting time:", min(waiting_queue))
#Probability that 1 server is available when job arrives
#Probability that 2 servers are available when job arrives
#Expected number of jobs processed by each server
#Expected idle time of each server during day
# print("Expected idle times per server:")
# print("Server 1 idle time:", statistics.mean(s1_idle_times))
# print("Server 2 idle time:", statistics.mean(s2_idle_times))
# print("Server 3 idle time:", statistics.mean(s3_idle_times))
# print("Server 4 idle time:", statistics.mean(s4_idle_times))
#Expected number of jobs remaining in system at 6:03pm

#Expected percentaje of jobs lost

