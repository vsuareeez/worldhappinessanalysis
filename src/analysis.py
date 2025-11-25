import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo de Seaborn
sns.set_theme(style="whitegrid")

# 1. PREPARACIÓN Y CARGA DE DATOS
# Ruta dinámica: busca el archivo csv en la carpeta 'data'
ruta_csv = os.path.join('data', 'world-happiness-report.csv')
ruta_guardado_png = 'images/'

# Carga de la base de datos
df = pd.read_csv(ruta_csv)

# Renombrar columnas para compatibilidad con el reporte 2021
column_mapping = {
    'Ladder score': 'Life Ladder',
    'Logged GDP per capita': 'Log GDP per capita',
    'Healthy life expectancy': 'Healthy life expectancy at birth'
}
df.rename(columns=column_mapping, inplace=True)

# 2. EXPLORACIÓN DE DATOS

# Resumen de Tipos de Datos y Nulos
df.info()

# Estadísticas Descriptivas
df.describe()

# Gráfico 1 (Seaborn): Histograma de 'Life Ladder'
plt.figure(figsize=(10, 6))
sns.histplot(df['Life Ladder'], kde=True, bins=30, color='blue')
plt.title('Distribución de "Life Ladder" (Felicidad) a Nivel Mundial')
plt.xlabel('Puntuación de Felicidad (Life Ladder)')
plt.ylabel('Frecuencia')
ruta_png1 = ruta_guardado_png + '01_seaborn_histograma_felicidad.png'
plt.savefig(ruta_png1)
plt.close() 

# 3. LIMPIEZA DE DATOS

# Eliminación de registros duplicados
df.drop_duplicates(inplace=True)

# Columnas a rellenar nulos
cols_a_rellenar = [
    'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth',
    'Freedom to make life choices', 'Generosity', 'Perceptions of corruption'
]

# Manejo de Valores Nulos: Media por país, luego media global
for col in cols_a_rellenar:
    df[col] = df.groupby('Country name')[col].transform(lambda x: x.fillna(x.mean()))
    media_global = df[col].mean()
    df[col] = df[col].fillna(media_global)

# Eliminación de filas con nulos en la variable objetivo principal
df.dropna(subset=['Life Ladder'], inplace=True)

# 4. TRANSFORMACIÓN DE DATOS

# Categorización de la Felicidad en 3 niveles (Bajo, Medio, Alto) usando cuantiles
df['Happiness Level'] = pd.qcut(df['Life Ladder'], 
                                q=3, 
                                labels=['Bajo', 'Medio', 'Alto'])

# Creación de la columna 'Affect Balance'
if 'Positive affect' in df.columns and 'Negative affect' in df.columns:
    df['Affect Balance'] = df['Positive affect'] - df['Negative affect']
    
# 5. VISUALIZACIÓN DE DATOS

# --- GRÁFICOS SEABORN ---

# Gráfico 2 (Seaborn): Mapa de Calor de Correlación
plt.figure(figsize=(12, 8))
columnas_numericas = df.select_dtypes(include=np.number)
matriz_corr = columnas_numericas.corr()
sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Mapa de Calor de Correlación (Seaborn)')
plt.tight_layout()
ruta_png2 = ruta_guardado_png + '02_seaborn_heatmap_correlacion.png'
plt.savefig(ruta_png2)
plt.close()

# Gráfico 3 (Seaborn): Gráfico de Dispersión (PIB vs Felicidad)
plt.figure(figsize=(12, 7))
sns.scatterplot(
    data=df,
    x='Log GDP per capita',
    y='Life Ladder',
    hue='Happiness Level',
    palette='viridis',
    alpha=0.7,
    s=50
)
plt.title('Relación entre PIB per Cápita y Felicidad (Seaborn)')
plt.xlabel('Log PIB per Cápita')
plt.ylabel('Puntuación de Felicidad (Life Ladder)')
plt.legend(title='Nivel de Felicidad')
ruta_png3 = ruta_guardado_png + '03_seaborn_scatterplot_pib.png'
plt.savefig(ruta_png3)
plt.close()


# --- GRÁFICOS MATPLOTLIB ---

# Gráfico 4 (Matplotlib): Gráfico de Líneas (Evolución Temporal de Sudamérica)
if 'year' in df.columns:
    paises_sudamerica = ['Chile', 'Argentina', 'Bolivia', 'Uruguay', 'Paraguay']
    df_sudamerica = df[df['Country name'].isin(paises_sudamerica)]

    plt.figure(figsize=(12, 7))
    ax = plt.gca()
    for pais in paises_sudamerica:
        datos_pais = df_sudamerica[df_sudamerica['Country name'] == pais].sort_values('year')
        ax.plot(datos_pais['year'], datos_pais['Life Ladder'], label=pais, marker='o')

    ax.set_title('Evolución de Felicidad en Países de Sudamérica (Matplotlib)')
    ax.set_xlabel('Año')
    ax.set_ylabel('Puntuación de Felicidad (Life Ladder)')
    ax.legend()
    ax.grid(True)
    ruta_png4 = ruta_guardado_png + '04_matplotlib_lineplot_evolucion.png'
    plt.savefig(ruta_png4)
    plt.close()
else:
    print("Advertencia: No se encontró la columna 'year'. Se omite el gráfico de evolución temporal.")

# Gráfico 5 (Matplotlib): Gráfico de Barras (Top 10 Países)
top_10_paises = df.groupby('Country name')['Life Ladder'].mean().nlargest(10).sort_values(ascending=True)

plt.figure(figsize=(12, 8))
plt.barh(top_10_paises.index, top_10_paises.values, color=sns.color_palette('plasma', n_colors=10))
plt.title('Top 10 Países con Mayor Felicidad Promedio (2005-2020) (Matplotlib)')
plt.xlabel('Puntuación de Felicidad Promedio')
plt.ylabel('País')
for index, value in enumerate(top_10_paises):
    plt.text(value, index, f' {value:.2f}')
plt.tight_layout()
ruta_png5 = ruta_guardado_png + '05_matplotlib_barplot_top10.png'
plt.savefig(ruta_png5)
plt.close()

# Gráfico 6 (Matplotlib): Gráfico de Torta (Distribución de Niveles)
if 'Happiness Level' in df.columns:
    conteo_niveles = df['Happiness Level'].value_counts()
    
    plt.figure(figsize=(8, 8))
    plt.pie(conteo_niveles.values, labels=conteo_niveles.index, autopct='%1.1f%%',
        colors=sns.color_palette('pastel'), startangle=90)
    plt.title('Distribución de Niveles de Felicidad (Bajo, Medio, Alto) (Matplotlib)')
    plt.axis('equal')
    ruta_png6 = ruta_guardado_png + '06_matplotlib_piechart_niveles.png'
    plt.savefig(ruta_png6)
    plt.close()



#Fuentes de Datos
#"""World Happiness Report (Kaggle): https://www.kaggle.com/datasets/ajaypalsinghlo/world-happiness-report-2021
#Documentación Utilizada: Enlaces a la documentación de las librerías utilizadas o documentación de la fuente.
#Documentación de Pandas: https://pandas.pydata.org/pandas-docs/stable/
#Documentación de Matplotlib:https://matplotlib.org/stable/contents.html
#Documentación de Seaborn: https://seaborn.pydata.org/
