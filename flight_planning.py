url = 'https://docs.google.com/spreadsheets/d/19BpApkKvozUBaMJO_V8tmwkCLwkJRkXi/'

from datetime import datetime, timedelta, time
import pandas as pd
from time import localtime
df_flights = pd.read_excel(url + 'export?format=xlsx', usecols='B:F', header=1)
df_zones = pd.read_excel(url + 'export?format=xlsx', usecols='H:I', header=1).dropna()

# Convertir zonas horarias a offset
zone_offset = {row['City']: int(row['Time Zone'].replace('GMT+', '')) for _, row in df_zones.iterrows()}

# Función para convertir hora local a UTC
def to_utc(local_time_input, city):
    # Si es datetime.datetime, extrae la hora
    if isinstance(local_time_input, datetime):
        local_time = local_time_input
    elif isinstance(local_time_input, time):
        local_time = datetime.combine(datetime.today(), local_time_input)
    elif isinstance(local_time_input, str):
        local_time = datetime.strptime(local_time_input, "%H:%M")
    else:
        raise ValueError(f"Formato de hora no reconocido: {type(local_time_input)}")

    offset = zone_offset[city]
    return local_time - timedelta(hours=offset)

# Agregar columnas de hora UTC
def add_utc_times(row):
    dep_utc = to_utc(row['Departure Time'], row['From'])

    # Si Duration es un objeto datetime.time, extraer horas y minutos
    duracion = row['Duration']
    if isinstance(duracion, time):
        h, m = duracion.hour, duracion.minute
    elif isinstance(duracion, str):
        h, m = map(int, duracion.split(':'))
    else:
        raise ValueError(f"Formato de duración no reconocido: {type(duracion)}")

    duration = timedelta(hours=h, minutes=m)
    arr_utc = dep_utc + duration
    return pd.Series({'Dep UTC': dep_utc, 'Arr UTC': arr_utc})

df_flights[['Dep UTC', 'Arr UTC']] = df_flights.apply(add_utc_times, axis=1)

# Rutas que queremos analizar
rutas = ['1,6', '3,9', '7']

# Resultado enriquecido
result = {
    'ID': [],
    'Duration': [],
    'Arrival Time (UTC)': [],
    'Arrival Time (Local)': []
}

for ruta in rutas:
    ids = list(map(int, ruta.split(',')))
    vuelos = df_flights[df_flights['ID'].isin(ids)].sort_values(by='Dep UTC')

    total_duracion = timedelta()

    for i in range(len(vuelos)):
        vuelo = vuelos.iloc[i]

        # Extraer duración
        duracion = vuelo['Duration']
        if isinstance(duracion, time):
            h, m = duracion.hour, duracion.minute
        elif isinstance(duracion, str):
            h, m = map(int, duracion.split(':'))
        else:
            raise ValueError(f"Formato de duración no reconocido: {type(duracion)}")

        duracion_vuelo = timedelta(hours=h, minutes=m)
        total_duracion += duracion_vuelo

        # Calcular espera si hay siguiente vuelo
        if i < len(vuelos) - 1:
            siguiente = vuelos.iloc[i + 1]
            espera = siguiente['Dep UTC'] - vuelo['Arr UTC']
            total_duracion += espera

    salida_inicial = vuelos.iloc[0]['Dep UTC']
    llegada_utc = salida_inicial + total_duracion

    ciudad_destino = vuelos.iloc[-1]['To']
    offset_destino = zone_offset[ciudad_destino]
    llegada_local = llegada_utc + timedelta(hours=offset_destino)

    result['ID'].append(ruta)
    result['Duration'].append(f"{total_duracion.seconds//3600}:{(total_duracion.seconds//60)%60:02d}")
    result['Arrival Time (UTC)'].append(llegada_utc.strftime('%H:%M UTC'))
    result['Arrival Time (Local)'].append(llegada_local.strftime('%H:%M') + f" ({ciudad_destino} local)")

# Mostrar resultado
df_resultado = pd.DataFrame(result)
print(df_resultado)
