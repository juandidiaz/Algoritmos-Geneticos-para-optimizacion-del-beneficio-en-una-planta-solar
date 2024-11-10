# Optimización de Beneficios en una Planta Solar usando Algoritmos Genéticos

Este proyecto implementa diversos algoritmos genéticos para maximizar las ganancias en la compra y venta de energía en una planta solar. Utilizando técnicas de optimización basadas en algoritmos evolutivos, se busca obtener soluciones eficientes para mejorar los beneficios de la planta.

## Descripción del Proyecto

Los algoritmos genéticos son métodos inspirados en la evolución natural y la selección genética que se aplican en problemas de optimización. Este proyecto implementa varias técnicas de algoritmos genéticos y variantes como **búsqueda local** y **CHC** (Cross-generational elitist selection, Heterogeneous recombination, and Cataclysmic mutation), enfocadas en la optimización de funciones multimodales.

## Archivos Principales

- **BusquedaLocal.py**: Contiene métodos de búsqueda local para mejorar soluciones de manera iterativa, explorando el vecindario de soluciones actuales.
- **CHC.py**: Implementación del algoritmo genético CHC, que utiliza estrategias avanzadas de recombinación y mutación para explorar el espacio de búsqueda.
- **GeneticoBasico.py**: Un algoritmo genético básico que sirve como punto de partida, proporcionando una implementación estándar de selección, cruce y mutación.
- **Multimodal.py**: Enfocado en optimización para problemas multimodales, permitiendo encontrar múltiples óptimos locales en la función objetivo.
- **base.py**: Define clases o funciones base utilizadas por los otros módulos del proyecto, estandarizando la funcionalidad y estructura de los algoritmos.
- **main.py**: Script principal que coordina la ejecución de los diferentes algoritmos y gestiona el flujo de optimización.

## Objetivo del Proyecto

El objetivo de este proyecto es maximizar los beneficios de una planta solar optimizando las decisiones de compra y venta de energía mediante algoritmos genéticos. Cada algoritmo explora diferentes enfoques y estrategias para encontrar soluciones óptimas y robustas en el espacio de búsqueda.

## Requisitos

- **Python 3** y las siguientes bibliotecas:
  - `numpy`
  - `matplotlib` (opcional, si se realizan visualizaciones)

Instala las dependencias con:

```bash
pip install numpy matplotlib
