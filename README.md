# 🌍 Análisis de Datos: Reporte Mundial de la Felicidad

## 📌 Descripción del Proyecto
Este proyecto de Minería de Datos analiza el *World Happiness Report* (2005-2020) para identificar qué factores socioeconómicos influyen más en la felicidad percibida de las naciones.

Se utilizó Python para realizar la limpieza de datos, imputación de valores nulos, ingeniería de características y visualización estadística.

## 🎯 Objetivos
* Identificar correlaciones entre variables económicas (PIB) y sociales con la felicidad ("Life Ladder").
* Analizar la evolución temporal de la felicidad en Sudamérica.
* Generar visualizaciones para facilitar la toma de decisiones basada en datos.

## 🛠 Tecnologías Utilizadas
* Python 3.x
* Pandas & NumPy: Manipulación y limpieza de datos (Manejo de nulos mediante imputación por media nacional).
* Seaborn & Matplotlib: Visualización de datos (Mapas de calor, Scatterplots, Series temporales).

## 📊 Hallazgos Clave
Basado en el análisis exploratorio:
1.  Economía y Salud: Existe una correlación fuerte positiva entre el PIB per cápita (0.80) y la Esperanza de Vida Saludable (0.75) con la felicidad.
2.  Factor Social: El soporte social es un pilar fundamental, superando a la libertad de elección.
3.  Corrupción: Es el factor con mayor impacto negativo (-0.42).
4.  Sudamérica: Se observa volatilidad en la región, con caídas notables en países como Chile (2018-2020), en contraste con la estabilidad de Uruguay.

## 📷 Visualizaciones Destacadas

### Correlación de Variables
![Heatmap](graficos/02_seaborn_heatmap_correlacion.png)
*Mapa de calor que evidencia la fuerte relación entre PIB, Apoyo Social y Felicidad.*

### PIB vs Felicidad
![Scatterplot](graficos/03_seaborn_scatterplot_pib.png)
*Los países con mayor PIB se concentran exclusivamente en niveles de felicidad "Alta".*

## 🚀 Cómo ejecutar este proyecto
1. Clonar el repositorio.
2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el script de análisis:
   ```bash
   python src/analysis.py
   ```

Proyecto desarrollado como parte de la asignatura de Minería de Datos - Ingeniería en Informática.
