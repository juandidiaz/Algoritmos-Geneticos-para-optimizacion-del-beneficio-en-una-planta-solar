import random
import statistics

import base as b
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
horas = range(0, 24)

L = 24
num_individuos_inicial = 22
iteraciones_sin_mejora = 500
alpha = 0.05
d = 8
granularidad = 8


def DistanciaHamming(solucion1, solucion2, granularidad):
    distancia = 0
    for i in range(len(solucion1)):
        if abs(solucion1[i] - solucion2[i]) > granularidad:
            distancia += 1
    return distancia


def BLX_alpha(padre1, padre2, alpha, granularidad):
    cambiar = 0
    hijo1 = padre1
    hijo2 = padre2

    for j in range(len(padre1)):
        if abs(padre1[j] - padre2[j] > granularidad):
            if cambiar == 0:
                hijo1[j] = padre2[j]
                cambiar = 1
            else:
                hijo2[j] = padre1[j]
                cambiar = 0
    hijos = []
    hijos.append(hijo1)
    hijos.append(hijo2)
    hijosDevolver = []
    for i in range(2):
        hijoCambiar = hijos[i]
        for j in range(len(padre1)):
            minimo = min(padre1[j], padre2[j]) - alpha * abs(padre1[j] - padre2[j])
            maximo = max(padre1[j], padre2[j]) + alpha * abs(padre1[j] - padre2[j])
            if minimo < -100:
                minimo = 100
            if maximo > 100:
                maximo = 100
            hijoCambiar[j] = int(np.random.uniform(minimo, maximo))
        hijosDevolver.append(hijoCambiar)

    return hijosDevolver[0], hijosDevolver[1]


def recombine(padres):
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

    return hijo1, hijo2


def selectS(p1, C, evaluacion, evaluacionHijos, r, pv, pc):
    poblacion = copy.copy(p1)
    peoresP1 = np.argsort(evaluacion)[:int(len(p1))]
    mejoresC = np.flip(np.argsort(evaluacionHijos)[:int(len(C))])
    peoresP1 = peoresP1.tolist()
    mejoresC = mejoresC.tolist()

    p11 = []
    mejoresC1 = []
    for i in range(len(peoresP1)):
        p11.append(copy.copy(p1[peoresP1[i]]))
    for i in range(len(mejoresC)):
        mejoresC1.append(copy.copy(C[mejoresC[i]]))
    iteraciones = min(len(p11), len(mejoresC1))
    for i in range(iteraciones):
        valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(p11[i], r, pv, pc)
        valor2, lista_bateria2, lista_beneficio2 = b.funcion_evaluacion(mejoresC1[i], r, pv, pc)
        if valor2 > valor:
            poblacion[i] = copy.copy(mejoresC1[i])
        else:
            poblacion[i] = copy.copy(p11[i])
    return poblacion


def ListasIguales(poblacion1, poblacion2):
    iguales = True
    for i in range(len(poblacion1)):
        if not (np.array_equal(poblacion1[i], poblacion2[i])):
            iguales = False
            break
    return iguales


def CHC(radiacion, pv, pc, L, num_individuos_ini, iter_sin_mejora, alpha, distanciaMaxima, granularidad, aleatorio):
    semillas = [123456, 678901, 9876538, 4920083, 763682]
    ListaEvaluaciones = []
    ListaFitness = []
    for semilla in semillas:
        np.random.seed(semilla)
        random.seed(semilla)
        GraficaFitness = []
        GraficaFitnessPeor = []
        t = 0
        d = L / 4
        evaluaciones = 0
        poblacion = []
        evaluacion = []
        reintentos = 0
        iteraciones = 0
        # INICIALIZAR POBLACION
        for i in range(num_individuos_ini):
            poblacion.append(copy.copy(b.generar_solucion_inicial()))
        # EVALUAR POBLACION
        for i in range(len(poblacion)):
            valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(poblacion[i], radiacion, pv, pc)
            evaluacion.append(valor)
            evaluaciones += 1
        mejorEncontrado = max(poblacion, key=lambda x: b.funcion_evaluacion(x, radiacion, pv, pc))
        valorMejorEncontrado, lista_bateriaMejorEncontrado, lista_beneficioMejorEncontrado = b.funcion_evaluacion(
            mejorEncontrado, radiacion, pv, pc)
        GraficaFitness.append(valorMejorEncontrado)

        peorEncontrado = min(poblacion, key=lambda x: b.funcion_evaluacion(x, radiacion, pv, pc))
        valorPeorEncontrado, lista_bateriaPeorEncontrado, lista_beneficioEncontrado = b.funcion_evaluacion(
            peorEncontrado, radiacion, pv, pc)
        GraficaFitnessPeor.append(valorPeorEncontrado)

        while t < iter_sin_mejora:
            iteraciones += 1
            # SELECTr, con esto obtenemos C(t)
            random.shuffle(poblacion)
            evaluacion = []
            for i in range(len(poblacion)):
                valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(poblacion[i], radiacion, pv, pc)
                evaluacion.append(valor)
                evaluaciones += 1

            # RECOMBINE, obtenemos C'(t)
            hijos = []
            insertados = 0
            for i in range(0, len(poblacion), 2):
                if DistanciaHamming(poblacion[i], poblacion[i + 1], granularidad) > distanciaMaxima:
                    padres = []
                    padres.append(poblacion[i])
                    padres.append(poblacion[i + 1])
                    hijo1, hijo2 = recombine(padres)
                    # hijo1,hijo2=BLX_alpha(padres[0], padres[0], alpha, granularidad)
                    hijos.append(copy.copy(hijo1))
                    hijos.append(copy.copy(hijo2))
                    insertados += 2
            if insertados == 0:
                d = 1
            # Evaluar hijos
            evaluacionHijos = []
            for i in range(len(hijos)):
                valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(hijos[i], radiacion, pv, pc)

                evaluacionHijos.append(valor)
                evaluaciones += 1

            poblacion2 = selectS(poblacion, hijos, evaluacion, evaluacionHijos, radiacion, pv, pc)
            evaluaciones += 2

            if ListasIguales(poblacion, poblacion2):
                d -= 1

            poblacion = copy.copy(poblacion2)
            mejor_individuo = max(poblacion, key=lambda x: b.funcion_evaluacion(x, radiacion, pv, pc))
            valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(mejor_individuo, radiacion, pv, pc)
            evaluaciones += 1

            if valor > valorMejorEncontrado:
                mejorEncontrado = copy.copy(mejor_individuo)
                valorMejorEncontrado = valor
                GraficaFitness.append(valorMejorEncontrado)
                t = 0
            else:
                t += 1
                GraficaFitness.append(valorMejorEncontrado)

            peor_individuo = min(poblacion, key=lambda x: b.funcion_evaluacion(x, radiacion, pv, pc))
            valorPeor, lista_bateriaPeor, lista_beneficioPeor = b.funcion_evaluacion(peor_individuo, radiacion, pv,
                                                                                     pc)
            evaluaciones += 1

            GraficaFitnessPeor.append(valorPeor)
            if d < 0:

                poblacion = []
                poblacion.append(copy.copy(mejorEncontrado))
                for i in range(num_individuos_ini - 1):
                    poblacion.append(copy.copy(b.generar_solucion_inicial()))
                d = L / 4
                reintentos += 1
                t = 0

        print("Se ha reintentado: ", reintentos)
        print("El mejor individuo es: ", mejorEncontrado)
        valor, lista_bateria, lista_beneficio = b.funcion_evaluacion(mejorEncontrado, radiacion, pv, pc)
        print("Fitness: ", valor)
        ListaEvaluaciones.append(evaluaciones)
        ListaFitness.append(valor)
        maximoIndice = GraficaFitness.index(max(GraficaFitness))
        fig, axes = plt.subplots()
        axes.plot(horas, lista_beneficio, "k", label="Beneficio")
        axes.set_xlabel("Horas")
        axes.set_title(f"Semilla:{semilla}")
        axes.set_ylabel("Beneficio(€)")
        axes.legend()
        axes.set_title(f"Semilla: {semilla}")

        twin_axes = axes.twinx()
        twin_axes.plot(horas, lista_bateria, "r", label="Bateria")
        twin_axes.set_ylabel("Batería(kWh)")
        twin_axes.legend()

        axes.set_ylim([-100, max(max(lista_beneficio), max(lista_bateria))])
        twin_axes.set_ylim([-100, max(max(lista_beneficio), max(lista_bateria))])

        plt.xticks(range(0, 24, 1))
        if not aleatorio:
            plt.savefig(f"RealesCHCIndividuo{semilla}")
            plt.show()
        else:
            plt.savefig(f"AleatoriosCHCIndividuo{semilla}")
            plt.show()

        fig2, axes2 = plt.subplots()
        X = [i for i in range(len(GraficaFitness))]
        axes2.plot(X, GraficaFitness, "k", label="Mejor individuo")
        axes2.plot(X, GraficaFitnessPeor, "r", label="Peor individuo")
        axes2.set_xlabel("Iteraciones")
        axes2.set_ylabel("Fitness")
        axes2.scatter(maximoIndice, valor, c='r', marker='x', label="Máximo")
        axes2.legend()
        plt.title(f"Fitness Semilla{semilla}")
        if not aleatorio:
            plt.savefig(f"RealesCHCFitness{semilla}")
            plt.show()
        else:
            plt.savefig(f"AleatorioCHCFitness{semilla}")
            plt.show()
    print("Ev. Medias: ", statistics.mean(ListaEvaluaciones))
    print("Ev. Mejor: ", min(ListaEvaluaciones))
    print("Desv. Ev: ", statistics.stdev(ListaEvaluaciones))
    print("Mejor Fitness: ", max(ListaFitness))
    print("Media Fitness: ", statistics.mean(ListaFitness))
    print("Desv. Fitness: ", statistics.stdev(ListaFitness))
