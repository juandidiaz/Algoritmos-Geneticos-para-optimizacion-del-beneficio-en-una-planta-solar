import random
import statistics

import base as b
import numpy as np
import matplotlib.pyplot as plt
import copy

num_individuos_ini = 23
iteraciones_maximas = 300
porcentaje_mutacion = 0.05
num_min_torneo = 3
rango_mutacion = 0.1
porcentaje_poblacion_seleccion = 0.35
porcentaje_poblacion_reemplazo = 0.3

real_pc = [26, 26, 25, 24, 23, 24, 25, 27, 30, 29, 34, 32, 31, 31, 25, 24, 25, 26, 34, 36, 39, 40, 38, 29]
real_pv = [24, 23, 22, 23, 22, 22, 20, 20, 20, 19, 19, 20, 19, 20, 22, 23, 22, 23, 26, 28, 34, 35, 34, 24]
real_r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

random_pc = [7, 7, 50, 25, 11, 26, 48, 45, 10, 14, 42, 14, 42, 22, 40, 34, 21, 31, 29, 34, 11, 37, 8, 50]
random_pv = [1, 3, 21, 1, 10, 7, 44, 35, 4, 1, 23, 12, 30, 7, 30, 4, 9, 10, 6, 9, 8, 27, 7, 10]
random_r = [274, 345, 605, 810, 252, 56, 964, 98, 77, 816, 68, 261, 841, 897, 75, 489, 833, 96, 117, 956, 970, 255, 74,
            926]
horas = range(0, 24)


def GeneticoBasico(r, pv, pc, num_individuos_inicial, it, aleatorio):
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
        num_individuos = num_individuos_inicial
        for i in range(num_individuos):
            poblacion.append(copy.copy(b.generar_solucion_inicial()))
        evaluacion = []
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
                                                                                                      pv, pc)
        evaluaciones += 1
        GraficaFitnessPeor.append(valorFitnessPeor)
        while t < it:
            padres = []
            num_individuos = len(poblacion)

            # SELECCION
            indicesPadres = []
            numero_torneo = max(3, int(porcentaje_poblacion_seleccion * num_individuos))
            padres = []
            seleccionados = set()
            for _ in range(2):
                while True:
                    torneo = random.sample(range(len(poblacion)), numero_torneo)
                    padre = max(torneo, key=lambda x: evaluacion[x])
                    if padre not in seleccionados:
                        padres.append(poblacion[padre])
                        indicesPadres.append(padre)
                        seleccionados.add(padre)
                        break

            # CRUCE
            hijos = []
            punto_cruce1 = random.randint(0, 23)
            punto_cruce2 = random.randint(0, 23)
            hijo1 = np.concatenate(
                (padres[0][:punto_cruce1], padres[1][punto_cruce1:punto_cruce2], padres[0][punto_cruce2:]), axis=None)
            hijo2 = np.concatenate(
                (padres[1][:punto_cruce1], padres[0][punto_cruce1:punto_cruce2], padres[1][punto_cruce2:]), axis=None)
            if len(hijo1) > 24:
                hijo1 = hijo1[:24]
            if len(hijo2) > 24:
                hijo2 = hijo2[:24]
            hijos.append(hijo1)
            hijos.append(hijo2)

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

            evaluacion = []
            for i in range(len(poblacion)):
                valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(poblacion[i], r, pv, pc)
                evaluacion = np.append(evaluacion, valor)
                evaluaciones += 1

            mejor_individuo = max(poblacion, key=lambda x: b.funcion_evaluacion(x, r, pv, pc))
            evaluaciones += len(poblacion)
            valorFitness, lista_bateriaFitness, lista_beneficioFitness = b.funcion_evaluacion(mejor_individuo, r, pv,
                                                                                              pc)
            evaluaciones += 1

            peor_individuo = min(poblacion, key=lambda x: b.funcion_evaluacion(x, r, pv, pc))
            evaluaciones += len(poblacion)
            valorFitnessPeor, lista_bateriaFitnessPeor, lista_beneficioFitnessPeor = b.funcion_evaluacion(
                peor_individuo, r, pv, pc)
            evaluaciones += 1
            if valorFitness > valorMejorEncontrado:
                valorMejorEncontrado = valorFitness
                t = 0
            else:
                t += 1
            GraficaFitness.append(valorMejorEncontrado)
            GraficaFitnessPeor.append(valorFitnessPeor)

        print("El mejor individuo es: ", mejor_individuo)
        valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(mejor_individuo, r, pv, pc)
        evaluaciones += 1
        ListaFitnessMejores.append(valor)
        ListaEvaluaciones.append(evaluaciones)
        print("Su beneficio es de: ", valor)
        fig, axes = plt.subplots()
        axes.plot(horas, lista_beneficio, "k", label="Beneficio")
        axes.set_xlabel("Horas")
        axes.set_title(f"Semilla: {semilla}")
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
            plt.savefig(f"RealesGeneticoBasicoIndividuo{semilla}")
            plt.show()
        else:
            plt.savefig(f"AleatoriosGeneticoBasicoIndividuo{semilla}")
            plt.show()

        fig2, axes2 = plt.subplots()
        X = [i for i in range(len(GraficaFitness))]
        axes2.plot(X, GraficaFitness, "k", label="Mejor Individuo")
        axes2.plot(X, GraficaFitnessPeor, "r", label="Peor individuo")
        axes2.set_xlabel("Iteraciones")
        axes2.set_ylabel("Fitness")
        axes2.legend()
        plt.title(f"Fitness Semilla{semilla}")
        if not aleatorio:
            plt.savefig(f"RealesGeneticoBasicoFitness{semilla}")
            plt.show()
        else:
            plt.savefig(f"AleatorioGeneticoBasicoFitness{semilla}")
            plt.show()
    return ListaEvaluaciones, ListaFitnessMejores
