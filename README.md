# Flight-Planning
![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)

- 🌟 Every Other Day Excel and Power Query Challenges No290🌟 * Author: Omid Motamedisedeh
 
    - Topic: Flight Route Analyzer!
 
 🔰 Este proyecto analiza rutas de vuelo entre ciudades con diferentes zonas horarias, calculando la duración total del viaje y la hora de llegada real en UTC y en hora local.
 
 🔗 Link to Excel file:
 👉 https://lnkd.in/g4MTvUPN

**My code in Python** 🐍 **for this challenge**
 🔗 https://github.com/vegacastilloe/Flight-Planning/blob/main/Flight_Planning.py




# ✈️ Flight Route Analyzer

Este proyecto analiza rutas de vuelo entre ciudades con diferentes zonas horarias, calculando la duración total del viaje y la hora de llegada real en UTC y en hora local.

## 📦 Datos

- **Flights**: contiene vuelos con hora de salida local, duración, origen y destino.
- **TimeZones**: contiene las zonas horarias de cada ciudad en formato GMT.

## 🧠 Lógica del análisis

1. Convierte la hora local de salida a UTC.
2. Calcula la duración de cada vuelo.
3. Suma los tiempos de espera entre vuelos.
4. Calcula la hora de llegada en UTC.
5. Convierte la hora de llegada a la zona horaria del destino final.

## 📊 Resultado

Una tabla con:
- ID de vuelos utilizados
- Duración total del viaje (vuelos + esperas)
- Hora de llegada en UTC
- Hora local de llegada en la ciudad destino

## 🛠️ Requisitos

- Python 3.8+
- pandas
- Archivo Excel con las hojas `Flights` y `TimeZones`

## 🚀 Ejecución

```bashpython
flight_planning.py
