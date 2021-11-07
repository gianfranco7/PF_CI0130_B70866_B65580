import math
import random as rd

from pandas.tseries import frequencies
from scipy import stats as sp

#Generacion de un numero aleatorio basado en la distribución
#De Poisson utilizando una funcion de densidad acumulativa inversa
def inverseCDF(t, _lambda):
    return -math.log(1 - t)/_lambda



#Generacion de tiempos entre llegadas en minutos de acuerdo a la cantidad de horas dada
def exponential_generator(_lambda):
    r = rd.random()
    inter_arrival_time = inverseCDF(r, _lambda)
    return inter_arrival_time



#Generacion de la lista completa de tiempos de llegada
def interarrival_times(t, _lambda):
    times = []
    while(True):
        inter_time = exponential_generator(_lambda)

        if inter_time + sum(times) > t:
            break
        times.append(inter_time)

    return times


#def gamma_random(alpha, lambd):
#    rand_num = rd.random()
#    rand_num = 
#    return rand_num


#Creacion de tiempo de servicio dependiendo del servidor a usar
def service_time_fromID(id):
    if id == 0:
        #r = np.random.gamma(7,1/3)
        r = sp.gamma.pdf(7, 1/3)
        
    elif id == 1:
        #r = np.random.gamma(5,1/2)
        r = sp.gamma.pdf(5,1/2)
    
    elif id == 2:
        #r = np.random.exponential(1/0.3)
        r = exponential_generator(1/0.3)

    elif id == 3:
        #r = rd.uniform(4,9)
        r = rd.uniform(4,9)

    return r / 60