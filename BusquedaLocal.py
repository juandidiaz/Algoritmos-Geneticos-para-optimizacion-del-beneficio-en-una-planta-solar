import matplotlib.pyplot as plt
import base as b
import statistics
import numpy as np
import random

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

semillas = [123456, 678901, 9876538, 4920083, 763682]

horas = range(0, 24)


# Busqueda Local Mejor
def busqueda_local_mejor(pv, pc, r, granularidad):
    BeneficiosTotales = []
    EvaluacionesTotales = []
    for i in range(len(semillas)):
        evaluaciones = 0
        np.random.seed(semillas[i])
        random.seed(semillas[i])
        GraficaFitness = []
        solucion_actual = b.generar_solucion_inicial()
        iteraciones = 0
        while (iteraciones < 5000):  # Fijar numero de iteraciones
            mejor_vecino = solucion_actual
            beneficioMejor, lista_batMejor, lista_benMejor = b.funcion_evaluacion(mejor_vecino, r, pv, pc)
            GraficaFitness.append(beneficioMejor)
            evaluaciones += 1
            pos = 0
            sumar = True
            for j in range(48):
                vecino = b.generar_vecino(solucion_actual, pos, sumar, granularidad)
                pos += 1
                if (pos == 24):
                    pos = 0
                    sumar = False
                beneficioPrimo, lista_batPrimo, lista_benPrimo = b.funcion_evaluacion(vecino, r, pv, pc)
                evaluaciones += 1
                if beneficioPrimo > beneficioMejor:
                    mejor_vecino = vecino
                    beneficioMejor, lista_batMejor, lista_benMejor = b.funcion_evaluacion(mejor_vecino, r, pv, pc)
                    evaluaciones += 1
            beneficioActual, lista_batActual, lista_benActual = b.funcion_evaluacion(solucion_actual, r, pv, pc)
            evaluaciones += 1
            iteraciones += 1
            # Si el beneficio del mejor vecino es mejor que el de la solucion actual,
            # la solucion actual pasa a ser ese vecino
            if beneficioMejor > beneficioActual:
                solucion_actual = mejor_vecino
            # Si el beneficio del mejor vecino es peor que el de la actual, salgo del while
            if beneficioMejor <= beneficioActual:
                break

        EvaluacionesTotales.append(evaluaciones)
        print(f"Solucion {i}: ", solucion_actual)
        beneficio, lista_bat, lista_ben = b.funcion_evaluacion(solucion_actual, r, pv, pc)
        BeneficiosTotales.append(beneficio)
        print("El beneficio ha sido de ", beneficio, " €")
        fig, axes = plt.subplots()
        axes.plot(horas, lista_ben, "k", label="Beneficio")
        axes.set_xlabel("Horas")
        axes.set_ylabel("Beneficio(€)")
        axes.legend()

        twin_axes = axes.twinx()
        twin_axes.plot(horas, lista_bat, "r", label="Bateria")
        twin_axes.set_ylabel("Batería(kWh)")
        twin_axes.legend()

        axes.set_ylim([-100, max(max(lista_ben), max(lista_bat))])
        twin_axes.set_ylim([-100, max(max(lista_ben), max(lista_bat))])
        plt.title(f"Búsqueda Local Mejor: Semilla {semillas[i]} y granularidad {granularidad}")

        plt.xticks(range(0, 24, 1))
        plt.savefig(f"IndividuoBusquedaLocal{semillas[i]}")
        plt.show()
        fig2, axes2 = plt.subplots()
        X = [i for i in range(len(GraficaFitness))]
        axes2.plot(X, GraficaFitness, "k", label="Fitness Busqueda Local")
        axes2.set_xlabel("Iteraciones")
        axes2.set_ylabel("Fitness")
        axes2.legend()
        plt.savefig(f"BusquedaLocalFitness{semillas[i]}")
        plt.show()
    print()
    print("EVMEDIAS: ", statistics.mean(EvaluacionesTotales))
    print("EVMEJOR: ", min(EvaluacionesTotales))
    print("EVDESV: ", round(statistics.stdev(EvaluacionesTotales), 2))
    print("MEDIA: ", round(statistics.mean(BeneficiosTotales), 2))
    print("DESVIACIÓN TÍPICA: ", round(statistics.stdev(BeneficiosTotales), 2))
    print("MEJOR RESULTADO: ", max(BeneficiosTotales))
    print()
