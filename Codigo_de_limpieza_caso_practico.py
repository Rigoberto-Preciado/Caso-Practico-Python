# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Cargar datos
who = pd.read_csv("/content/drive/MyDrive/Recursos Colab/who.csv")
population = pd.read_csv("/content/drive/MyDrive/Recursos Colab/population.csv")

# Limpieza de datos
# Manejo de valores faltantes
who.loc[who.country == "Namibia", "iso2"] = "NA"
who = who.fillna(0)

# Transformación de datos
who2 = who.melt(id_vars=["country", "year", "iso2", "iso3"], var_name="variable", value_name="cases")

# Asignar género
who2["gender"] = np.where(who2["variable"].str.contains("m"), "masculino", "femenino")

# Funciones para asignar grupos
def asignar_groupedad(valor):
    if "014" in valor: return "0-14"
    elif "1524" in valor: return "15-24"
    elif "2534" in valor: return "25-34"
    elif "3544" in valor: return "35-44"
    elif "4554" in valor: return "45-54"
    elif "5564" in valor: return "55-64"
    elif "65" in valor: return "65+"

def asignar_metodo(valor):
    if "rel" in valor: return "recaída"
    elif "sn" in valor: return "esputo pulmonar negativo"
    elif "sp" in valor: return "esputo pulmonar positivo"
    elif "ep" in valor: return "extrapulmonar"

who2["agegroup"] = who2["variable"].apply(asignar_groupedad)
who2["method"] = who2["variable"].apply(asignar_metodo)

# Combinar con datos de población
df = pd.merge(left=who2, right=population, how="inner", on=["country", "year"])

# Calcular tasas de incidencia
by_country_year = df.groupby(["country", "year"], as_index=False).agg(
    {"cases":"sum", "population":"max"}
)
by_country_year["incidencia"] = 100000 * by_country_year["cases"] / by_country_year["population"]

by_year = by_country_year.groupby("year", as_index=False).agg(
    {"cases":"sum", "population": "sum"}
)
by_year["incidencia"] = 100_000 * by_year["cases"] / by_year["population"]

# Guardar datos limpios
df.to_csv("tuberculosis_clean.csv", index=False)
by_country_year.to_csv("tuberculosis_by_country_year.csv", index=False)
by_year.to_csv("tuberculosis_by_year.csv", index=False)