import random
import statistics

import base as b
import numpy as np
import matplotlib.pyplot as plt
import copy
import math

real_pc = [26, 26, 25, 24, 23, 24, 25, 27, 30, 29, 34, 32, 31, 31, 25, 24, 25, 26, 34, 36, 39, 40, 38, 29]
real_pv = [24, 23, 22, 23, 22, 22, 20, 20, 20, 19, 19, 20, 19, 20, 22, 23, 22, 23, 26, 28, 34, 35, 34, 24]
real_r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

random_pc = [7, 7, 50, 25, 11, 26, 48, 45, 10, 14, 42, 14, 42, 22, 40, 34, 21, 31, 29, 34, 11, 37, 8, 50]
random_pv = [1, 3, 21, 1, 10, 7, 44, 35, 4, 1, 23, 12, 30, 7, 30, 4, 9, 10, 6, 9, 8, 27, 7, 10]
random_r = [274, 345, 605, 810, 252, 56, 964, 98, 77, 816, 68, 261, 841, 897, 75, 489, 833, 96, 117, 956, 970, 255, 74,
            926]
horas = range(0, 24)

num_individuos_ini = 23
iteraciones_sin_mejora = 100
porcentaje_mutacion = 0.2
num_min_torneo = 3
rango_mutacion = 0.1
porcentaje_poblacion_seleccion = 0.2
porcentaje_poblacion_reemplazo = 0.2
probabilidad_cruce = 0.8

real_pc = [26, 26, 25, 24, 23, 24, 25, 27, 30, 29, 34, 32, 31, 31, 25, 24, 25, 26, 34, 36, 39, 40, 38, 29]
real_pv = [24, 23, 22, 23, 22, 22, 20, 20, 20, 19, 19, 20, 19, 20, 22, 23, 22, 23, 26, 28, 34, 35, 34, 24]
real_r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

random_pc = [7, 7, 50, 25, 11, 26, 48, 45, 10, 14, 42, 14, 42, 22, 40, 34, 21, 31, 29, 34, 11, 37, 8, 50]
random_pv = [1, 3, 21, 1, 10, 7, 44, 35, 4, 1, 23, 12, 30, 7, 30, 4, 9, 10, 6, 9, 8, 27, 7, 10]
random_r = [274, 345, 605, 810, 252, 56, 964, 98, 77, 816, 68, 261, 841, 897, 75, 489, 833, 96, 117, 956, 970, 255, 74,
            926]
horas = range(0, 24)
radio = 300
kappa = 6
P = 5


def DistanciaHamming(solucion1, solucion2):
    return np.sum(solucion1 != solucion2)


def distancia_euclidea(solucion1, solucion2):
    distancia = 0
    for i in range(len(solucion1)):
        distancia += (solucion1[i] - solucion2[i]) ** 2
    return int(math.sqrt(distancia))


def Multimodal(r, pv, pc, num_individuos_inicial, radio, kappa, P, it, aleatorio):
    semillas = [123456, 678901, 9876538, 4920083, 763682]
    ListaEvaluaciones = []
    ListaFitnessMejores = []
    for semilla in semillas:
        evaluaciones = 0
        GraficaFitness = []
        GraficaFitnessPeor = []
        np.random.seed(semilla)
        random.seed(semilla)
        t = 0
        poblacion = []
        # Generacion de poblacion
        num_individuos = num_individuos_inicial
        for i in range(num_individuos):
            poblacion.append(copy.copy(b.generar_solucion_inicial()))
        evaluacion = []
        # Evaluacion de la poblacion
        for i in range(len(poblacion)):
            valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(poblacion[i], r, pv, pc)
            evaluacion.append(valor)
            evaluaciones += 1
        mejor_individuo = max(poblacion, key=lambda x: b.funcion_evaluacion(x, r, pv, pc))
        evaluaciones += num_individuos
        valorFitness, lista_bateriaFitness, lista_beneficioFitness = b.funcion_evaluacion(mejor_individuo, r, pv, pc)
        evaluaciones += 1
        valorMejorEncontrado = valorFitness
        GraficaFitness.append(valorFitness)

        peor_individuo = min(poblacion, key=lambda x: b.funcion_evaluacion(x, r, pv, pc))
        evaluaciones += len(poblacion)
        valorFitnessPeor, lista_bateriaFitnessPeor, lista_beneficioFitnessPeor = b.funcion_evaluacion(peor_individuo, r,
                                                                                                      pv,
                                                                                                      pc)
        GraficaFitnessPeor.append(valorFitnessPeor)
        contador = 0
        while t < it:
            contador += 1
            padres = []
            num_individuos = len(poblacion)

            # Clearing
            if (contador % int((P * (num_individuos_inicial / 2)))) == 0:
                poblacion = [x for _, x in sorted(zip(evaluacion, poblacion), key=lambda pair: pair[0], reverse=True)]
                evaluacion = sorted(evaluacion, reverse=True)

                for i in range(len(poblacion)):
                    if evaluacion[i] > 0:
                        num_ganadores = 1
                        for j in range(i + 1, len(poblacion)):
                            if evaluacion[j] > 0 and (distancia_euclidea(poblacion[i], poblacion[j]) < radio):
                                if num_ganadores < kappa:
                                    num_ganadores += 1
                                else:
                                    evaluacion[j] = 0
                supervivientes = []
                for i in range(len(poblacion)):
                    if evaluacion[i] > 0:
                        supervivientes.append(copy.copy(poblacion[i]))

                while len(supervivientes) < num_individuos_inicial:
                    evaluacionSupervivientes = []
                    for i in range(len(supervivientes)):
                        valor, bateria, beneficio = b.funcion_evaluacion(supervivientes[i], r, pv, pc)
                        evaluacionSupervivientes.append(valor)
                    padres = []
                    seleccionados = set()
                    for _ in range(2):
                        while True:
                            torneo = random.sample(range(len(supervivientes)), 3)
                            padre = max(torneo, key=lambda x: evaluacionSupervivientes[x])

                            if padre not in seleccionados:
                                seleccionados.add(padre)
                                padres.append(supervivientes[padre])
                                break
                    punto_cruce1 = random.randint(0, 23)
                    punto_cruce2 = random.randint(0, 23)
                    hijo1 = np.concatenate(
                        (padres[0][:punto_cruce1], padres[1][punto_cruce1:punto_cruce2], padres[0][punto_cruce2:]),
                        axis=None)
                    hijo2 = np.concatenate(
                        (padres[1][:punto_cruce1], padres[0][punto_cruce1:punto_cruce2], padres[1][punto_cruce2:]),
                        axis=None)
                    if len(hijo1) > 24:
                        hijo1 = hijo1[:24]
                    if len(hijo2) > 24:
                        hijo2 = hijo2[:24]
                    supervivientes.append(hijo1)
                    supervivientes.append(hijo2)
                poblacion = copy.copy(supervivientes)

            # SELECCION
            evaluacion = []

            indicesPadres = []
            numero_torneo = max(3, int(porcentaje_poblacion_seleccion * len(poblacion)))
            for i in range(len(poblacion)):
                valor, bateria, beneficio = b.funcion_evaluacion(poblacion[i], r, pv, pc)
                evaluacion.append(valor)
            padres = []
            seleccionados = set()
            for _ in range(2):
                while True:
                    torneo = random.sample(range(len(poblacion)), numero_torneo)
                    padre = max(torneo, key=lambda x: evaluacion[x])
                    if padre not in seleccionados:
                        padres.append(poblacion[padre])
                        seleccionados.add(padre)
                        indicesPadres.append(padre)
                        break
            hijos = []
            if random.random() < 0.8:
                # CRUCE
                punto_cruce1 = random.randint(0, 23)
                punto_cruce2 = random.randint(0, 23)
                hijo1 = np.concatenate(
                    (padres[0][:punto_cruce1], padres[1][punto_cruce1:punto_cruce2], padres[0][punto_cruce2:]),
                    axis=None)
                hijo2 = np.concatenate(
                    (padres[1][:punto_cruce1], padres[0][punto_cruce1:punto_cruce2], padres[1][punto_cruce2:]),
                    axis=None)
                if len(hijo1) > 24:
                    hijo1 = hijo1[:24]
                if len(hijo2) > 24:
                    hijo2 = hijo2[:24]
                hijos.append(hijo1)
                hijos.append(hijo2)
            else:
                hijos.append(padres[0])
                hijos.append(padres[1])

            # MUTACION
            for hijo in hijos:
                if random.random() < porcentaje_mutacion:
                    posicion = random.randint(0, 23)
                    mutacion = random.uniform(0, rango_mutacion * hijo[posicion])
                    if random.random() >= 0.5:
                        if hijo[posicion] + mutacion <= 100:
                            hijo[posicion] += mutacion
                        else:
                            hijo[posicion] = 100
                    else:
                        if hijo[posicion] - mutacion >= -100:
                            hijo[posicion] -= mutacion
                        else:
                            hijo[posicion] = -100

            # REEMPLAZO
            numero_torneo = max(3, int(porcentaje_poblacion_reemplazo * num_individuos))
            torneo = random.sample(range(len(poblacion)), numero_torneo)
            ganador = min(torneo, key=lambda x: evaluacion[x])
            valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(poblacion[ganador], r, pv, pc)
            evaluaciones += 1
            for i in range(len(hijos)):
                valorHijo, lista_bateriaHijo, lista_beneficioHijo = b.funcion_evaluacion(hijos[i], r, pv, pc)
                if valorHijo > valor:
                    poblacion[ganador] = copy.copy(hijos[i])
                    break

            mejor_individuo = max(poblacion, key=lambda x: b.funcion_evaluacion(x, r, pv, pc))
            evaluaciones += len(poblacion)
            valorFitness, lista_bateriaFitness, lista_beneficioFitness = b.funcion_evaluacion(mejor_individuo, r, pv,
                                                                                              pc)
            if valorFitness > valorMejorEncontrado:
                valorMejorEncontrado = valorFitness
                t = 0
            else:
                t += 1

            peor_individuo = min(poblacion, key=lambda x: b.funcion_evaluacion(x, r, pv, pc))
            evaluaciones += len(poblacion)
            valorFitnessPeor, lista_bateriaFitnessPeor, lista_beneficioFitnessPeor = b.funcion_evaluacion(
                peor_individuo, r, pv,
                pc)

            evaluaciones += 1
            GraficaFitness.append(valorFitness)
            GraficaFitnessPeor.append(valorFitnessPeor)
            evaluacion = []
            for i in range(len(poblacion)):
                valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(poblacion[i], r, pv, pc)
                evaluacion = np.append(evaluacion, valor)
                evaluaciones += 1

        poblacion = [x for _, x in sorted(zip(evaluacion, poblacion), key=lambda pair: pair[0], reverse=True)]
        evaluacion = sorted(evaluacion, reverse=True)

        for i in range(len(poblacion)):
            if evaluacion[i] > 0:
                num_ganadores = 1
                for j in range(i + 1, len(poblacion)):
                    if evaluacion[j] > 0 and (distancia_euclidea(poblacion[i], poblacion[j]) < radio):
                        if num_ganadores < 1:
                            num_ganadores += 1
                        else:
                            evaluacion[j] = 0
        supervivientes = []
        for i in range(len(poblacion)):
            if evaluacion[i] > 0:
                supervivientes.append(poblacion[i])

        print("Distintas soluciones")
        for i in range(len(supervivientes)):
            print(f"Superviviente {i}: ", supervivientes[i])
            valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(supervivientes[i], r, pv, pc)
            print("Su valor es: ", valor)

        print("El mejor individuo es: ", mejor_individuo)
        valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(mejor_individuo, r, pv, pc)
        evaluaciones += 1
        ListaFitnessMejores.append(valor)
        ListaEvaluaciones.append(evaluaciones)
        print("Su beneficio es de: ", valor)
        fig, axes = plt.subplots()
        axes.plot(horas, lista_beneficio, "k", label="Beneficio")
        axes.set_xlabel("Horas")
        axes.set_title(f"Semilla:{semilla}")
        axes.set_ylabel("Beneficio(€)")
        axes.legend()

        twin_axes = axes.twinx()
        twin_axes.plot(horas, lista_bateria, "r", label="Bateria")
        twin_axes.set_ylabel("Batería(kWh)")
        twin_axes.legend()

        axes.set_ylim([-100, max(max(lista_beneficio), max(lista_bateria))])
        twin_axes.set_ylim([-100, max(max(lista_beneficio), max(lista_bateria))])

        plt.xticks(range(0, 24, 1))
        if not aleatorio:
            plt.savefig(f"RealesMultimodalIndividuo{semilla}")
            plt.show()
        else:
            plt.savefig(f"AleatoriosMultimodalIndividuo{semilla}")
            plt.show()

        fig2, axes2 = plt.subplots()
        X = [i for i in range(len(GraficaFitness))]
        axes2.plot(X, GraficaFitness, "k", label="Mejor individuo")
        axes2.plot(X, GraficaFitnessPeor, "r", label="Peor individuo")
        axes2.set_xlabel("Iteraciones")
        axes2.set_ylabel("Fitness")
        axes2.legend()
        plt.title(f"Fitness Semilla {semilla}")
        if not aleatorio:
            plt.savefig(f"RealesMultimodalFitness{semilla}")
            plt.show()
        else:
            plt.savefig(f"AleatorioMultimodalFitness{semilla}")
            plt.show()
    return ListaEvaluaciones, ListaFitnessMejores
