from exportar_excel import generar_excel
from io import BytesIO

import streamlit as st
import pandas as pd
import os
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime
import joblib
import pandas as pd


# Archivo para guardar los viajes
ARCHIVO_VIAJES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "viajes.csv"
)

ARCHIVO_TEMPERATURAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "registro_temperaturas.csv"
)
# Ruta del modelo de Machine Learning
ARCHIVO_MODELO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "machine_learning",
    "modelo_riesgo_v2.pkl"
)
# Cargar modelo de Machine Learning
@st.cache_resource
def cargar_modelo():
    return joblib.load(ARCHIVO_MODELO)

# Guardar historial de temperaturas
def guardar_historial_temperatura(fecha_hora, camion_id, viaje_id, temperatura_actual, temperatura_requerida):
    nuevo_registro = pd.DataFrame([{
        "fecha_hora": fecha_hora,
        "camion_id": camion_id,
        "viaje_id": viaje_id,
        "temperatura_actual": temperatura_actual,
        "temperatura_requerida": temperatura_requerida
    }])

    nuevo_registro.to_csv(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "historial_temperaturas.csv"),
        mode="a",
        header=False,
        index=False
    )


# Buscar coordenadas de una ciudad
@st.cache_data(ttl=86400)
def buscar_coordenadas(ciudad):
    url = "https://nominatim.openstreetmap.org/search"

    parametros = {
        "q": f"{ciudad}, Chile",
        "format": "json",
        "limit": 1
    }

    encabezados = {
        "User-Agent": "RutaFrioIA/1.0 (prototipo educativo)"
    }

    try:
        respuesta = requests.get(
            url,
            params=parametros,
            headers=encabezados,
            timeout=15
        )
        respuesta.raise_for_status()
        datos = respuesta.json()

        if datos:
            return float(datos[0]["lat"]), float(datos[0]["lon"])

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

    return None

# Calcular distancia y tiempo por carretera
@st.cache_data(ttl=3600)
def calcular_ruta(origen, destino):
    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{origen[1]},{origen[0]};"
        f"{destino[1]},{destino[0]}"
    )

    try:
        respuesta = requests.get(
            url,
            params={"overview": "false"},
            timeout=20
        )
        respuesta.raise_for_status()
        datos = respuesta.json()

        if datos.get("code") == "Ok" and datos.get("routes"):
            ruta = datos["routes"][0]
            distancia_km = ruta["distance"] / 1000
            tiempo_horas = ruta["duration"] / 3600
            return distancia_km, tiempo_horas

    except (requests.RequestException, ValueError, KeyError):
        return None

    return None


# Configuración de la aplicación
st.set_page_config(
    page_title="RutaFrío IA",
    page_icon="🚛",
    layout="wide"
)

# Encabezado principal
st.title("🚛❄️ RutaFrío IA")
st.subheader("Sistema Inteligente de Transporte Refrigerado")

st.success("Bienvenido al sistema RutaFrío IA")

st.write(
    "Plataforma para planificar viajes, controlar "
    "la temperatura y prevenir pérdidas de alimentos "
    "durante el transporte refrigerado."
)

st.divider()

# Menú principal
st.sidebar.title("🚛 Menú principal")

opcion = st.sidebar.radio(
    "Seleccione una opción:",
    [
        "Inicio",
        "Registrar transporte",
        "Planificar rutas",
        "Control de temperatura",
        "Predicción de riesgos",
        "Reportes"
    ]
)

if opcion == "Inicio":
    st.header("Panel principal")
    st.info("Seleccione una opción del menú para comenzar.")

elif opcion == "Registrar transporte":
    st.header("Registro de transporte")
    with st.form("formulario_transporte"):
        patente = st.text_input("Patente del camión")
        conductor = st.text_input("Nombre del conductor")

        producto = st.selectbox(
            "Producto transportado",
            [
                "Frutas",
                "Verduras",
                "Carnes",
                "Pescados",
                "Lácteos",
                "Congelados",
                "Otros"
            ]
        )

        origen = st.text_input("Ciudad de origen")
        destino = st.text_input("Ciudad de destino")

        temperatura = st.number_input(
            "Temperatura requerida (°C)",
            min_value=-30.0,
            max_value=30.0,
            value=4.0,
            step=0.5
        )

        guardar = st.form_submit_button("Registrar transporte")

    if guardar:
        if patente.strip() and conductor.strip() and origen.strip() and destino.strip():

            nuevo_viaje = pd.DataFrame([{
                "Patente": patente.strip().upper(),
                "Conductor": conductor.strip(),
                "Producto": producto,
                "Origen": origen.strip(),
                "Destino": destino.strip(),
                "Temperatura": temperatura
            }])

            try:
                existe = os.path.exists(ARCHIVO_VIAJES)

                nuevo_viaje.to_csv(
                    ARCHIVO_VIAJES,
                    mode="a",
                    header=not existe,
                    index=False,
                    encoding="utf-8-sig" if not existe else "utf-8"
                )

                st.success("¡Transporte guardado correctamente!")
                st.dataframe(nuevo_viaje, hide_index=True)

            except OSError as error:
                st.error(f"No se pudo guardar el viaje: {error}")

        else:
            st.warning("Complete todos los campos obligatorios.")



elif opcion == "Planificar rutas":
    st.header("🗺️ Planificación de rutas")

    st.write(
        "Ingrese los datos del recorrido para planificar "
        "el transporte de productos refrigerados."
    )

    with st.form("formulario_rutas"):

        origen_ruta = st.text_input(
            "Ciudad de origen",
            placeholder="Ejemplo: Santiago"
        )

        destino_ruta = st.text_input(
            "Ciudad de destino",
            placeholder="Ejemplo: Valparaíso"
        )

        producto_ruta = st.selectbox(
            "Producto transportado",
            [
                "Frutas",
                "Verduras",
                "Carnes",
                "Pescados",
                "Lácteos",
                "Congelados",
                "Otros"
            ]
        )

        temperatura_ruta = st.number_input(
            "Temperatura requerida (°C)",
            min_value=-30.0,
            max_value=30.0,
            value=4.0,
            step=0.5
        )

        calcular = st.form_submit_button(
            "🚛 Planificar viaje"
        )

    if calcular or st.session_state.get("mostrar_ruta", False):
        st.session_state["mostrar_ruta"] = True
        if origen_ruta.strip() and destino_ruta.strip():
            st.success("Datos de la ruta ingresados correctamente.")

            st.write("Origen:", origen_ruta)
            st.write("Destino:", destino_ruta)
            st.write("Producto:", producto_ruta)
            st.write("Temperatura requerida:", temperatura_ruta, "°C")


            st.subheader("📍 Resultado de la planificación")
            coordenadas_origen = buscar_coordenadas(origen_ruta)
            coordenadas_destino = buscar_coordenadas(destino_ruta)


        if coordenadas_origen and coordenadas_destino:
            resultado = calcular_ruta(
                coordenadas_origen,
                coordenadas_destino
            )

            if resultado:
                distancia, tiempo = resultado
                st.session_state["distancia_ruta"] = distancia
                st.session_state["tiempo_ruta"] = tiempo

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Distancia por carretera",
                        f"{distancia:.1f} km"
                    )

                with col2:
                    st.metric(
                        "Tiempo estimado",
                        f"{tiempo:.1f} horas"
                    )
                    st.subheader("🗺️ Mapa de la ruta")
                    mapa = folium.Map(
                    location=coordenadas_origen,
                    zoom_start=8
                )
                    folium.Marker(
                    coordenadas_origen,
                    popup=f"Origen: {origen_ruta}",
                    icon=folium.Icon(color="green")
                ).add_to(mapa)
                    folium.Marker(
                    coordenadas_destino,
                    popup=f"Destino: {destino_ruta}",
                    icon=folium.Icon(color="red")
                ).add_to(mapa)
                    folium.PolyLine(
                    [coordenadas_origen, coordenadas_destino],
                    color="blue",
                    weight=4
                ).add_to(mapa)
                    st_folium(mapa, width=700, height=450)
            else:
                st.warning("No se pudo calcular la ruta.")
        else:
            st.warning(
                "No se encontraron las coordenadas de las ciudades."
            )

            st.write(
                "El siguiente paso será conectar el sistema "
                "con un servicio de mapas y rutas."
            )
            
       


elif opcion == "Control de temperatura":
    st.header("Control de temperatura")
    if os.path.exists(ARCHIVO_VIAJES):
        viajes_disponibles = pd.read_csv(ARCHIVO_VIAJES)
        if not viajes_disponibles.empty:
            st.success("Viajes disponibles para control de temperatura.")
            opciones_viajes = [
                f"{fila['Patente']} - {fila['Producto']} - {fila['Destino']}"
                for _, fila in viajes_disponibles.iterrows()
            ]

            viaje_seleccionado = st.selectbox(
                "Seleccionar transporte",
                opciones_viajes
            )
        else:
            st.warning("No existen transportes registrados.")
            viaje_seleccionado = None
    else:
        st.warning("No se encontró el archivo de viajes.")
        viaje_seleccionado = None
            
        
    st.write("Aquí supervisaremos la temperatura de la carga.")
    temperatura_actual = st.number_input(
        "Temperatura actual de la carga (°C)",
        min_value=-30.0,
        max_value=40.0,
        value=4.0,
        step=0.5
    )

    temperatura_requerida = st.number_input(
        "Temperatura requerida del producto (°C)",
        min_value=-30.0,
        max_value=40.0,
        value=4.0,
        step=0.5
    )

    diferencia_control = abs(
        temperatura_actual - temperatura_requerida
    )

    st.metric(
        "Diferencia de temperatura",
        f"{diferencia_control:.1f} °C"
    )
    
    
    tolerancia_advertencia = 1.0
    tolerancia_critica = 3.0

    if diferencia_control <= tolerancia_advertencia:
        st.success("🟢 Temperatura normal: carga protegida.")

    elif diferencia_control <= tolerancia_critica:
        st.warning(
            "🟡 Advertencia: revisar la refrigeración. "
            f"Desviación de {diferencia_control:.1f} °C."
        )

    else:
        st.error(
            "🔴 ALERTA CRÍTICA: revisar inmediatamente "
            "el sistema de refrigeración. "
            f"Desviación de {diferencia_control:.1f} °C."
        )



    
    if st.button("💾 Guardar temperatura"):
        nuevo_registro = pd.DataFrame([{
            "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "viaje_id": viaje_seleccionado.split(" - ")[0] if viaje_seleccionado else "",
            "temperatura_actual": temperatura_actual,
            "temperatura_requerida": temperatura_requerida
        }])
        nuevo_registro["nivel_riesgo"] = "Pendiente"

        nuevo_registro.to_csv(
            ARCHIVO_TEMPERATURAS,
            mode="a",
            header=not os.path.exists(ARCHIVO_TEMPERATURAS),
            index=False
        )
        # Guardar también en el historial
        guardar_historial_temperatura(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            viaje_seleccionado.split(" - ")[0] if viaje_seleccionado else "",
            viaje_seleccionado if viaje_seleccionado else "",
            temperatura_actual,
            temperatura_requerida
        )

        st.success("✅ Temperatura guardada correctamente.")   

    st.subheader("📋 Historial de temperaturas")

    if os.path.exists(ARCHIVO_TEMPERATURAS):
        historial = pd.read_csv(ARCHIVO_TEMPERATURAS)

        if viaje_seleccionado:
            patente_seleccionada = viaje_seleccionado.split(" - ")[0]
            historial = historial[
                historial["viaje_id"] == patente_seleccionada
            ]
      
    

        if not historial.empty:
            st.dataframe(
                historial,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Todavía no hay temperaturas registradas.")
    else:
        st.info("Todavía no existe un historial de temperaturas.")                

elif opcion == "Predicción de riesgos":
    st.header("Predicción de riesgos")
    st.write("Evaluación del riesgo del transporte refrigerado.")
    viaje_riesgo = None
    temperatura_registrada = None
    if os.path.exists(ARCHIVO_VIAJES):
        viajes_riesgo = pd.read_csv(ARCHIVO_VIAJES)
        if not viajes_riesgo.empty:
            opciones_riesgo = viajes_riesgo["Patente"].tolist()
            viaje_riesgo = st.selectbox("Seleccionar camión", opciones_riesgo)
            datos_camion = viajes_riesgo[
                     viajes_riesgo["Patente"] == viaje_riesgo
                ].iloc[0]
            st.success(f"Camión seleccionado: {datos_camion['Patente']}")
            if os.path.exists(ARCHIVO_TEMPERATURAS):
                temperaturas = pd.read_csv(ARCHIVO_TEMPERATURAS)
                temperaturas_camion = temperaturas[
                    temperaturas["viaje_id"] == viaje_riesgo
                ]

                if not temperaturas_camion.empty:
                    st.subheader("🌡️ Temperaturas del camión")
                    st.dataframe(
                        temperaturas_camion,
                        hide_index=True
                    )
                    ultimo_registro = temperaturas_camion.iloc[-1]
                    temperatura_registrada = float(ultimo_registro["temperatura_actual"])   
                    st.write("Temperatura recuperada del historial:", temperatura_registrada)             
        else:
            st.warning("No hay camiones registrados.")
    else:
        st.warning("No se encontró el archivo de viajes.")    

    distancia_riesgo = st.number_input(
        "Distancia del viaje (km)",
        
        value=float(st.session_state.get("distancia_ruta", 150.0)),
        step=10.0
    )
    tiempo_riesgo = st.number_input(
        "Tiempo estimado del viaje (horas)",
        min_value=0.0,
        value=float(st.session_state.get("tiempo_ruta", 3.0)),
        step=0.5
    )
    temperatura_riesgo = st.number_input(
        "Temperatura actual de la carga (°C)",
        min_value=-30.0,
        max_value=40.0,
        value=float(temperatura_registrada) if temperatura_registrada is not None else 4.0,
        step=0.5,
        key=f"temperatura_riesgo_{viaje_riesgo}"
    )
    temperatura_objetivo = st.number_input(
        "Temperatura requerida del producto (°C)",
        min_value=-30.0,
        max_value=40.0,
        value=4.0,
        step=0.5
    )
    retraso_riesgo = st.number_input("Retraso estimado (minutos)", min_value=0, value=0, step=5)
    evaluar_riesgo = st.button("🔍 Evaluar riesgo del transporte")
    if evaluar_riesgo:
        diferencia_temperatura = abs(
            temperatura_riesgo - temperatura_objetivo
        )
        modelo_ml = cargar_modelo()
        datos_ml = pd.DataFrame([{
            "distancia_km": distancia_riesgo,
            "tiempo_horas": tiempo_riesgo,
            "retraso_minutos": retraso_riesgo,
            "temperatura_actual": temperatura_riesgo,
            "temperatura_requerida": temperatura_objetivo,
            "desviacion_temperatura": diferencia_temperatura
        }])
        # Predecir nivel de riesgo con Machine Learning
        prediccion_ml = modelo_ml.predict(datos_ml)[0]

        # Preparar el nivel de riesgo para el historial
        nivel_riesgo_predicho = str(prediccion_ml)

         # Guardar riesgo del camion seleccionado
        if os.path.exists(ARCHIVO_TEMPERATURAS):
            registros = pd.read_csv(ARCHIVO_TEMPERATURAS)

            if not registros.empty:
                coincidencias = registros.index[
                    registros["viaje_id"].astype(str) == str(viaje_riesgo)
                ]

                if len(coincidencias) > 0:
                    ultima_fila = coincidencias[-1]
                    registros.loc[
                        ultima_fila, "nivel_riesgo"
                    ] = nivel_riesgo_predicho

                    registros.to_csv(
                        ARCHIVO_TEMPERATURAS,
                        index=False
                    )

        # Mostrar resultado de la inteligencia artificial
        if prediccion_ml == "Bajo":
            st.success("🟢 Machine Learning: Riesgo bajo")
            st.info("Recomendación: mantener el control periódico de la temperatura y verificar que el equipo de refrigeración funcione correctamente.")
        elif prediccion_ml == "Medio":
            st.warning("🟡 Machine Learning: Riesgo medio")
            st.info("Recomendación: revisar la refrigeración y controlar nuevamente la temperatura de la carga.")
        else:
            st.error("🔴 Machine Learning: Riesgo alto")

            st.info("Recomendación: verificar el equipo de refrigeración, comprobar la temperatura de la carga y avisar al responsable antes de continuar el transporte.")
        st.subheader("Resultado de la evaluación")
        st.metric(
            "Diferencia de temperatura",
            f"{diferencia_temperatura:.1f} °C"
        )
        if diferencia_temperatura <= 1:
                st.success("🟢 Riesgo por temperatura: BAJO. Temperatura cercana a la requerida.")
        elif diferencia_temperatura <= 3:
                st.warning("🟡 Riesgo por temperatura: MEDIO. Revisar la refrigeración.")

        else:
                st.error("🔴 Riesgo por temperatura: ALTO. Revisar urgentemente la temperatura.")
                    
        if tiempo_riesgo > 4 and diferencia_temperatura > 1:
            st.warning(
                "⚠️ Atención: viaje prolongado con desviación "
                "de temperatura. Revisar la cadena de frío."
            )
          

elif opcion == "Reportes":
    st.header("Reportes")
    if os.path.exists(ARCHIVO_VIAJES):
        viajes = pd.read_csv(ARCHIVO_VIAJES)
        reporte_completo = viajes.copy()
        if os.path.exists(ARCHIVO_TEMPERATURAS):
                temperaturas = pd.read_csv(ARCHIVO_TEMPERATURAS)
                temperaturas["viaje_id"] = temperaturas["viaje_id"].astype(str)
                viajes["Patente"] = viajes["Patente"].astype(str)
                temperaturas = temperaturas.sort_values("fecha_hora")
                ultimas_temperaturas = temperaturas.drop_duplicates(subset="viaje_id", keep="last")
                reporte_completo = viajes.merge(
                    ultimas_temperaturas,
                    left_on="Patente",
                    right_on="viaje_id",
                    how="left",
                    suffixes=("", "_registro")
                )


        st.success("Registros de transporte encontrados")
        st.metric("Total de viajes registrados", len(viajes))

        st.dataframe(
           reporte_completo,
           use_container_width=True,
            hide_index=True
        )


  
        st.download_button(
            label="📊 Descargar reporte Excel",
            data=generar_excel(reporte_completo),
            file_name="reporte_rutafrio.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    else:
        st.info("Todavía no existen viajes registrados.")
