import streamlit as st
import pandas as pd
import numpy as np

st.title("Border Freight - Cotizador")
st.write("Este cotizador esta diseñado para subir un archivo de rutas y evaluar los precios que contiene")

#We will first create a dictionary with distances that we assign each route
km = {"Reynosa, TAM - San Luis Potosi, SLP": 670, 
      "Reynosa, TAM - Monterrey, NLE": 200,
      "Ramos Arizpe, COA - Reynosa, TAM": 300,
      "Queretaro, QRO - Reynosa, TAM": 800}

#We will then create a variable to store our price per km 
cost_per_km = 25.3

#We will prompt the user to upload a file 
uploaded_file = st.file_uploader("Sube un archivo de Excel", type=["xlsx"])

if uploaded_file is not None:
      route_data = pd.read_excel(uploaded_file)
      st.write("Este es el Archivo Cargado")
      st.dataframe(route_data)
else: 
      st.warning("Por favor sube un archivo de Excel para continuar")
