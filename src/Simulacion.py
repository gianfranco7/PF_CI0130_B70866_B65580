import statistics
import pandas as pd
from Funciones import *

# Variables importantes de la simulacion
SIMULATION_RUNS = 1000
SIMULATION_HOURS = 10
WAIT_THRESHOLD = 6 / 60
ARRIVAL_TIMES = 30
REJECTED_JOBS = 0

RUN_DATAFRAMES = []
work_sum = [0, 0, 0, 0]
work_time_total = [0, 0, 0, 0]

for i in range(SIMULATION_RUNS):
    # El array de servidores contiene el tiempo en que se realizo
    # la ejecucion final de cada uno, se explica más
    # adelante en el comentario de TEORIA
    servers_last_finished_times = [0, 0, 0, 0]
    number_of_works_by_server = [0, 0, 0, 0]
    last_arrival_time = 0
    interarrival_time = interarrival_times(SIMULATION_HOURS, ARRIVAL_TIMES)

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
            number_of_works_by_server[min_index] += 1
            work_time_total[min_index] += service_time

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

    #Suma de todos los trabajos en la simulacion
    for i in range(0, 4):
        work_sum[i] += number_of_works_by_server[i]
    
    #Creacion del dataframe para la simulacion
    df = pd.DataFrame(data={
        'Interarrival': interarrival_times_list, 'Arrival Time': arrival_times_list,
         'Initial Service Time': start_times_list, 'Wait Time': wait_times_list,
          'Service Time': service_times_list, 'Final Time': finish_times_list, 'System Time': system_times_list
    })

    RUN_DATAFRAMES.append(df)


meanDataframe = get_mean_dataset(RUN_DATAFRAMES, SIMULATION_RUNS)

#Expected waiting time for a randomly selected job
expected_waiting_time = statistics.mean(meanDataframe['Mean Wait Time'])

#Expected response time
expected_response_time = statistics.mean(meanDataframe['Mean System Time'])

#Expected Queue length (Lq) = (Waiting queue)Wq * lambda
expected_queue_length = expected_waiting_time * 30

#Expected maximum waiting time
expected_max_waiting_time = statistics.mean(meanDataframe['Max Wait Time'])

#Expected maximum lenght of a queue


#Probability that at least one server is available

#Probability that at least two servers are available

#Number of jobs processed by each server
mean_server_jobs = [w / SIMULATION_RUNS for w in work_sum]

#The expected time each server is idle
expected_idle_time = [10 - (t / SIMULATION_RUNS) for t in work_time_total]

#Expected number of jobs still remaining in the sytstem at 6:03 pm
mean_job_overtime = statistics.mean(meanDataframe['Overtime Jobs'])

#Expected percentage of jobs that left the queue prematurely
expected_rejected_jobs = REJECTED_JOBS * 100 / sum(work_sum)

#print(meanDataframe)

data = f'''-----------------------------------------------------------------------------------------------------

                               ANALISIS BASE
Tiempo de espera promedio para un trabajo seleccionado aleatoriamente:      {expected_waiting_time:.4f}
Tiempo de respuesta esperado:                                               {expected_response_time:.4f}
Tamaño de cola esperado:                                                    {expected_queue_length:.4f}
Tiempo de espera maximo esperado en un día de 10 horas:                     {expected_max_waiting_time:.4f}
Tamaño maximo esperado de la cola en un dia de 10 horas:                               
Probabilidad de que al menos un servidor se encuentre disponible:
Probabilidad de que al menos 2 servidores se encuentren disponibles:
Cantidad esperada de trabajos procesados por cada servidor:                 I: {mean_server_jobs[0]:.4f}   II: {mean_server_jobs[1]:.4f}   III: {mean_server_jobs[2]:.4f}   IV: {mean_server_jobs[3]:.4f} 
Tiempo que cada servidor se encuentra inactivo durante el día:              I: {expected_idle_time[0]:.4f}   II: {expected_idle_time[1]:.4f}   III: {expected_idle_time[2]:.4f}   IV: {expected_idle_time[3]:.4f}
Cantidad de trabajos aun en el sistema a las 6:03pm:                        {mean_job_overtime:.4f}
Porcentage de trabajos que abandonan la cola prematuramente:                {expected_rejected_jobs:.4f}%                

-----------------------------------------------------------------------------------------------------'''

print(data)