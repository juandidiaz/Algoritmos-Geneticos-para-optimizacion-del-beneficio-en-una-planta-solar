import Multimodal as M
import GeneticoBasico as G
import CHC as C
import BusquedaLocal as BL
import statistics

# Parametros Basico
num_individuos_ini = 23
iteraciones_maximas = 300
porcentaje_mutacion = 0.2
num_min_torneo = 3
rango_mutacion = 0.1
porcentaje_poblacion_seleccion = 0.2
porcentaje_poblacion_reemplazo = 0.2
probabilidad_cruce = 0.8

# Parametros CHC
L = 24
num_individuos_inicialCHC = 22
iteraciones_sin_mejora = 500
alpha = 0.3
d = 8
granularidad = 8

# Parametros multimodal
iteraciones_sin_mejora_multimodal = 100
radio = 300
kappa = 6
P = 5

real_pc = [26, 26, 25, 24, 23, 24, 25, 27, 30, 29, 34, 32, 31, 31, 25, 24, 25, 26, 34, 36, 39, 40, 38, 29]
real_pv = [24, 23, 22, 23, 22, 22, 20, 20, 20, 19, 19, 20, 19, 20, 22, 23, 22, 23, 26, 28, 34, 35, 34, 24]
real_r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

random_pc = [7, 7, 50, 25, 11, 26, 48, 45, 10, 14, 42, 14, 42, 22, 40, 34, 21, 31, 29, 34, 11, 37, 8, 50]
random_pv = [1, 3, 21, 1, 10, 7, 44, 35, 4, 1, 23, 12, 30, 7, 30, 4, 9, 10, 6, 9, 8, 27, 7, 10]
random_r = [274, 345, 605, 810, 252, 56, 964, 98, 77, 816, 68, 261, 841, 897, 75, 489, 833, 96, 117, 956, 970, 255, 74,
            926]
horas = range(0, 24)

print("DATOS REALES GENÉTICO BÁSICO")
listaE, listaF = G.GeneticoBasico(real_r, real_pv, real_pc, num_individuos_ini, iteraciones_maximas, False)
print("Ev. Medias: ", statistics.mean(listaE))
print("Ev. Mejor: ", min(listaE))
print("Desv. Ev: ", statistics.stdev(listaE))
print("Mejor Fitness: ", max(listaF))
print("Media Fitness: ", statistics.mean(listaF))
print("Desv. Fitness: ", statistics.stdev(listaF))

print("DATOS ALEATORIOS GENÉTICO BÁSICO")
listaE, listaF = G.GeneticoBasico(random_r, random_pv, random_pc, num_individuos_ini, iteraciones_maximas, True)
print("Ev. Medias: ", statistics.mean(listaE))
print("Ev. Mejor: ", min(listaE))
print("Desv. Ev: ", statistics.stdev(listaE))
print("Mejor Fitness: ", max(listaF))
print("Media Fitness: ", statistics.mean(listaF))
print("Desv. Fitness: ", statistics.stdev(listaF))

print("DATOS REALES CHC")
C.CHC(real_r, real_pv, real_pc, L, num_individuos_inicialCHC, iteraciones_sin_mejora, alpha, d, granularidad, False)
print("DATOS ALEATORIOS CHC")
C.CHC(random_r, random_pv, random_pc, L, num_individuos_inicialCHC, iteraciones_sin_mejora, alpha, d, granularidad,
      True)

print("DATOS REALES MULTIMODAL")
listaE, listaF = M.Multimodal(real_r, real_pv, real_pc, num_individuos_ini, radio, kappa, P,
                              iteraciones_sin_mejora_multimodal, False)
print("Ev. Medias: ", statistics.mean(listaE))
print("Ev. Mejor: ", min(listaE))
print("Desv. Ev: ", statistics.stdev(listaE))
print("Mejor Fitness: ", max(listaF))
print("Media Fitness: ", statistics.mean(listaF))
print("Desv. Fitness: ", statistics.stdev(listaF))

print("DATOS ALEATORIOS MULTIMODAL")
listaE, listaF = M.Multimodal(random_r, random_pv, random_pc, num_individuos_ini, radio, kappa, P,
                              iteraciones_sin_mejora_multimodal, True)
print("Ev. Medias: ", statistics.mean(listaE))
print("Ev. Mejor: ", min(listaE))
print("Desv. Ev: ", statistics.stdev(listaE))
print("Mejor Fitness: ", max(listaF))
print("Media Fitness: ", statistics.mean(listaF))
print("Desv. Fitness: ", statistics.stdev(listaF))

print("DATOS REALES BÚSQUEDA LOCAL")
BL.busqueda_local_mejor(real_pv, real_pc, real_r, 5)
print("DATOS ALEATORIOS BÚSQUEDA LOCAL")
BL.busqueda_local_mejor(random_pv, random_pc, random_r, 5)
