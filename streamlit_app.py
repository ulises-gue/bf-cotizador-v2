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
      route_data = pd.read_excel(uploaded_file, header = 1)
      st.write("Este es el Archivo Cargado")
      st.dataframe(route_data)
      #We will create a new column named Ruta that will combine the origen and destino column with a dash
      route_data["Ruta"] = route_data["Origen"] + " - " + route_data["Destino"]

      #We will create a new column named Distancia that will look for the route in the dictionary we created 
      #and return its distance
      route_data["Distancia"] = route_data["Ruta"].map(km)

      #We will create a column that will determine the route type depending on the distance
      route_data["Tipo de Ruta"] = np.where(route_data["Distancia"] <= 400, "Tramo Corto", "Tramo Largo")

      #We will create a column that will determine wether the route is outbound or returning
      route_data["Sentido"] = np.where(route_data["Origen"] == "Reynosa, TAM", "Salida", "Retorno")

      #We will create an array for the price and distance to calculate the price per km and create a column
      price_array = np.array(route_data["Precio"])
      distance_array = np.array(route_data["Distancia"])
      price_per_km = price_array / distance_array
      route_data["Precio por KM"] = price_per_km

      #We will create a loop to calculate route profitability and create a 
      profit = []
      profit_no_format = []
      for i in range(len(distance_array)):
            profit_margin = ((price_array[i] - (distance_array[i] * cost_per_km))/price_array[i])
            profit_no_format.append(profit_margin)
            profit_margin_formatted = f"{profit_margin:.1%}"
            profit.append(profit_margin_formatted)
      route_data["Utilidad"] = profit

      #We will create a loop to evaluate whether or not the route should be taken based on profit ranges
      evaluation = []
      for i in range(len(profit_no_format)):
            if route_data["Tipo de Ruta"][i] == "Tramo Corto":
                  if route_data["Sentido"][i] == "Salida":
                      if profit_no_format[i] >= 0.36:
                            evaluation.append("Si")
                      else:
                            evaluation.append("No")
            else:
                  if profit_no_format[i] >= 0.49:
                        evaluation.append("Si")
                  else:
                        evaluation.append("No")
            if route_data["Tipo de Ruta"][i] == "Tramo Largo":
                  if route_data["Sentido"][i] == "Salida":
                        if profit_no_format[i] >= 0.15:
                              evaluation.append("Si")
                        else:
                              evaluation.append("No")
                  else:
                        if profit_no_format[i] >= 0.33:
                              evaluation.append("Si")
                        else:
                              evaluation.append("No")
                              
      route_data["Evaluacion"] = evaluation
      
      #We will create a new data frame with the columns we want
      route_download = pd.DataFrame(route_data, columns = ["Ruta", "Tipo de Ruta", "Sentido", 
                                                           "Distancia", "Precio", "Precio por KM", 
                                                           "Utilidad", "Evaluacion"])
            
      st.write("---")
      st.write("Evaluacion de Rutas:")
      st.dataframe(route_download)

else: 
      st.warning("Por favor sube un archivo de Excel para continuar")





