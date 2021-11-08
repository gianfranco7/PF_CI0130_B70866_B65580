import math
import random as rd

from pandas.tseries import frequencies
from scipy import stats as sp
import numpy as np

#Generacion de un numero aleatorio basado en la distribución
#De Poisson utilizando una funcion de densidad acumulativa inversa
def inverseExpCDF(t, _lambda):
    return -math.log(t)/_lambda



#Generacion de tiempos entre llegadas en minutos de acuerdo a la cantidad de horas dada
def exponential_generator(_lambda):
    r = rd.random()
    inter_arrival_time = inverseExpCDF(r, _lambda)
    return inter_arrival_time

def gamma_generator(alpha, _lambda):
    r = rd.random()
    for i in range(1, alpha):
        rtmp = rd.random()
        r *= rtmp
        
    variate = -1/(_lambda*alpha) * np.log(r)
    return variate

#Generacion de la lista completa de tiempos de llegada
def interarrival_times(t, _lambda):
    times = []
    while(True):
        inter_time = exponential_generator(_lambda)

        if inter_time + sum(times) > t:
            break
        times.append(inter_time)

    return times

#Creacion de tiempo de servicio dependiendo del servidor a usar
def service_time_fromID(id):
    if id == 0:
        r = gamma_generator(7,1/3)
    elif id == 1:
        r = gamma_generator(5,1/2)
    elif id == 2:
        r = exponential_generator(1/0.3)
    elif id == 3:
        r = rd.uniform(4,9)

    return r / 60


#        l = []
#        for i in range(0, 1000):
#            x = service_time_fromID(1)
#            print(x)
#            l.append(x)
#        import statistics
#        print(statistics.mean(l))