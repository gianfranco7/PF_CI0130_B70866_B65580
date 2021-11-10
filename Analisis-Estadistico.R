#Importacion del dataset en formato CSV, este archivo fue producido por python
#Desde la biblioteca Pandas
df <- read.csv("Dataframe.csv")
dayDF <- read.csv("1-dayDF.csv")
  
#Resumen de los datos
summary(df)




plot(df$Mean.Interarrival)


#Media de tiempos entre llegada:
mean(df$Mean.Interarrival)

#Desviacion estandard de tiempos entre llegadas:
sd(df$Mean.Interarrival)


#Variacion de tiempos entre llegadas:
var(df$Mean.Interarrival)






plot(dayDF$Service.Time)
boxplot(dayDF$Service.Time)

#Media de tiempos de servicio en un dia aleatorio:
mean(dayDF$Service.Time)

#Desviacion estandard de tiempos de servicio en un dia aleatorio:
sd(dayDF$Service.Time)

#Variacion de tiempos de servicio en un dia aleatorio
var(dayDF$Service.Time)


