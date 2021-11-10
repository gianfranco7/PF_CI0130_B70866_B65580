import math
import random as rd
import statistics
import numpy as np
import pandas as pd


#Generacion de un numero aleatorio basado en la distribución
#De Poisson utilizando una funcion de densidad acumulativa inversa exponencial
def inverseExpCDF(t, _lambda):
    return -math.log(t)/_lambda



#Generacion de tiempos utilizando la funcion anterior, asignamos el valor aleatorio faltante
def exponential_generator(_lambda):
    r = rd.random()
    inter_arrival_time = inverseExpCDF(r, _lambda)
    return inter_arrival_time



#Generacion de numeros aleatorios usando el metodo inverso para Gamma
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


#Creacion de un dataset de medias para cada categoría
def get_mean_dataset(dataset_list, range):
    meanDataframe = pd.DataFrame(index = np.arange(range), columns=['Mean Interarrival', 'Mean Wait Time', 'Max Wait Time',
     'Mean Service Time', 'Mean System Time', 'Overtime Jobs'])
    index = 0
    for df in dataset_list:
        interarrival_mean = statistics.mean(df['Interarrival'])
        wait_time_mean = statistics.mean(df['Wait Time'])
        max_wait_time = max(df['Wait Time'])
        service_time_mean = statistics.mean(df['Service Time'])
        system_time_mean = statistics.mean(df['System Time'])    
        overtime = sum(map(lambda x : x > 10.05, df['Final Time']))
        meanDataframe.loc[index] = [interarrival_mean, wait_time_mean, max_wait_time, 
         service_time_mean, system_time_mean, overtime]
        index += 1
    return meanDataframe



#Calculo de ro / encontrar el sistema ocupado
def ro(_lambda, _micro, s):
    return _lambda / (_micro * s)


#Probabilidad de que haya 0 clientes en el sistema con s servidores
def P0(_micro, _lambda, s):
    prob = 0
    for n in range(s):
        prob += (((_lambda/_micro) ** n) / math.factorial(n))
        
    prob += (((_lambda/_micro) ** s) / (math.factorial(s) * (1 - ro(_lambda, _micro, s))))
    prob = prob ** -1
        
    return prob


#Probabilidad de que haya n clientes en el sistema para s servidores
def Pn(_micro, _lambda, s, n):

    if n > 0 and n < s:
        result = (((_lambda/_micro)**n)/math.factorial(n))*P0(_micro, _lambda, s) 

    elif n >= s:
        result = (((_lambda/_micro)**n)/(math.factorial(n)*(s**(n -s ))))*P0(_micro, _lambda, s) 

    return result


#Calculo de tamaño de cola con multiples servidores 
def Lq(_micro, _lambda, s):
    result = ((_lambda / _micro) ** s) * P0(_micro, _lambda, s) * ro(_micro, _lambda, s)
    result /= math.factorial(s) * (1 - ro(_micro, _lambda, s)) ** 2
    return result