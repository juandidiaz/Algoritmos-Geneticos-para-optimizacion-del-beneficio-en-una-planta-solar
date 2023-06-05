import numpy as np
import matplotlib.pyplot as plt
import copy

real_pc = [26, 26, 25, 24, 23, 24, 25, 27, 30, 29, 34, 32, 31, 31, 25, 24, 25, 26, 34, 36, 39, 40, 38, 29]
real_pv = [24, 23, 22, 23, 22, 22, 20, 20, 20, 19, 19, 20, 19, 20, 22, 23, 22, 23, 26, 28, 34, 35, 34, 24]
real_r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

random_pc = [7, 7, 50, 25, 11, 26, 48, 45, 10, 14, 42, 14, 42, 22, 40, 34, 21, 31, 29, 34, 11, 37, 8, 50]
random_pv = [1, 3, 21, 1, 10, 7, 44, 35, 4, 1, 23, 12, 30, 7, 30, 4, 9, 10, 6, 9, 8, 27, 7, 10]
random_r = [274, 345, 605, 810, 252, 56, 964, 98, 77, 816, 68, 261, 841, 897, 75, 489, 833, 96, 117, 956, 970, 255, 74,
            926]

extension = 1000
capacidad_bateria = 300
rendimiento = 0.2


# Generar un array aleatorio de tamaño 24. En cada posición habrá
# un numero entre -100 y 100
def generar_solucion_inicial():
    init_solution = np.random.randint(-100, 100, size=24)
    return init_solution


def funcion_evaluacion(solucion, radiacion, pv, pc):
    beneficio = 0
    bateria = 0
    lista_bateria = []
    lista_beneficio = []

    for i in range(len(solucion)):
        bateria += radiacion[i] * rendimiento
        if bateria > capacidad_bateria:
            sobrante = bateria - capacidad_bateria
            beneficio += pv[i] * sobrante
            bateria = capacidad_bateria
        # Caso Vender

        if solucion[i] >= 0:
            vender = (solucion[i] / 100) * bateria
            beneficio += pv[i] * vender
            bateria -= vender
        # Caso comprar
        else:
            comprar = (solucion[i] / 100) * (capacidad_bateria - bateria)
            beneficio += pc[i] * comprar
            bateria -= comprar
        if bateria > capacidad_bateria:
            bateria = capacidad_bateria
        if i < 23:
            lista_beneficio.append(round(beneficio / 100, 2))
            lista_bateria.append(bateria)

    if bateria > 0:
        vender = bateria
        beneficio += pv[-1] * vender
        bateria -= vender
    beneficio = round(beneficio / 100, 2)
    lista_bateria.append(bateria)
    lista_beneficio.append(beneficio)

    return beneficio, lista_bateria, lista_beneficio

def generar_vecino(solucion, pos, sumar,granularidad):
    vecino = copy.copy(solucion)

    if (sumar):

        if (vecino[pos] + granularidad <= 100):
            vecino[pos] += granularidad
        else:
            vecino[pos] = 100
    else:

        if (vecino[pos] - granularidad >= -100):
            vecino[pos] -= granularidad
        else:
            vecino[pos] = -100
    return vecino
