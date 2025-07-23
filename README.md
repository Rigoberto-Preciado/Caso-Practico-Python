# Caso-Practico-Python
En este proyecto se analizará la base de datos de la Organización Mundial de la Salud, en especifico datos de tuberculosis.
# Contexto
Los datos han llegado con la información más reciente y necesita prepararlos para mostrar la información a los líderes de la organización. 
# Objetivo.
El objetivo de la junta es entender la situación actual de tuberculosis, y las tendencias por región e identificar países que han sido casos de éxito y aquellos que necesiten mayor apoyo con la gestión de la enfermedad. 

Tenga en mente las metas de la ONU para terminar con la Tuberculosis para 2025: 

● Reducción en la tasa de incidencia del 50% 2015 vs 2025. 

● Reducción en 75% el número de muertes 2015 vs 2025

# Principales Analisis Realizados y Conclusiónes

## Código de limpieza de datos - código en Python 

- Cargar archivos CSV

inmport padas as pd
who_df= pd.read_csv("/content/drive/MyDrive/Recursos Colab/who.csv")
population_df = pd.read_csv("/content/drive/MyDrive/Recursos Colab/population.csv")

- Convertir columnas anchas en formato largo

who_long = who_df.melt(
    id_vars=["country", "iso2", "iso3", "year"],
    var_name="indicator",
    value_name="cases"
)

- Eliminar valores nulos
  
who_long = who_long.dropna(subset=["cases"])

- Filtrar indicadores que comienzan con 'new'
  
who_long = who_long[who_long["indicator"].str.startswith("new")]

- Quitar el prefijo 'new' y los guiones bajos
  
who_long["indicator"] = who_long["indicator"].str.replace("new", "", regex=False)
who_long["indicator"] = who_long["indicator"].str.replace("_", "", regex=False)

- Extraer tipo, sexo y edad desde el string del indicador
  
who_long["type"] = who_long["indicator"].str.extract(r"([a-z]+)")
who_long["sex"] = who_long["indicator"].str.extract(r"([mf])")
who_long["age"] = who_long["indicator"].str.extract(r"(\d{2,3})")

- Eliminar columna original
  
who_long = who_long.drop(columns=["indicator"])

- Unir con el archivo de población
  
combined_df = pd.merge(who_long, population_df, on=["country", "year"], how="left")

- Calcular tasa de incidencia por cada 100,000 habitantes
  
combined_df["incidence_rate"] = (combined_df["cases"] / combined_df["population"]) * 100000

-Exportar datos limpios a CSV

combined_df.to_csv("datos_limpios_tb.csv", index=False)

print("Datos limpios guardados como 'datos_limpios_tb.csv'")

## Análisis exploratorio - formato libre, entrega en PDF 

## Lámina con resumen ejecutivo - máximo 2 láminas, entrega en PDF
