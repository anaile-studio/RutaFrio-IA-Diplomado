# RutaFrío IA
## Sistema Inteligente de Transporte Refrigerado

### 1. Descripción del proyecto

RutaFrío IA es una aplicación desarrollada en Python y Streamlit para apoyar la gestión del transporte de alimentos perecibles que requieren refrigeración.

El sistema busca reducir los riesgos asociados a retrasos en las entregas, variaciones de temperatura y posibles pérdidas de mercadería.

Integra herramientas de cálculo de rutas, registro de viajes, monitoreo de temperaturas y modelos de Machine Learning para clasificar el nivel de riesgo de las operaciones de transporte.

### 2. Objetivo general

Desarrollar un sistema inteligente que permita apoyar la planificación y supervisión del transporte refrigerado, utilizando análisis de datos y Machine Learning para identificar situaciones de riesgo y facilitar la toma de decisiones.
## 3. Problema que resuelve RutaFrío IA

El transporte de alimentos perecibles requiere mantener condiciones adecuadas de temperatura durante todo el trayecto.

Los retrasos provocados por congestión vehicular, accidentes, fallas mecánicas o problemas en los equipos de refrigeración pueden comprometer la calidad de los productos transportados.

Estas situaciones generan riesgos de pérdidas económicas, deterioro de mercadería e incumplimiento de los plazos de entrega.

RutaFrío IA propone apoyar la solución de estos problemas mediante:

- Cálculo de distancias y tiempos estimados de viaje.
- Registro y seguimiento de los viajes.
- Control de temperaturas de la carga.
- Identificación de desviaciones de temperatura.
- Clasificación del riesgo mediante Machine Learning.
- Generación de alertas e informes para apoyar las decisiones.

### 4. Funcionamiento y características del sistema

RutaFrío IA es una aplicación interactiva desarrollada con Python y Streamlit.

Sus principales funcionalidades son:

#### 4.1. Planificación de rutas
Permite ingresar puntos de origen y destino para calcular la distancia por carretera y el tiempo estimado del recorrido.

#### 4.2. Registro de viajes
Permite registrar información de los viajes y conservar un historial para su posterior análisis.

#### 4.3. Control de temperaturas
Permite registrar la temperatura de la carga, compararla con la temperatura requerida e identificar desviaciones.

#### 4.4. Evaluación del riesgo
Utiliza un modelo de Machine Learning para clasificar situaciones de riesgo en tres categorías:

- Bajo
- Medio
- Alto

#### 4.5. Alertas y reportes
Incorpora funcionalidades para generar alertas, consultar registros históricos y preparar reportes que apoyen la supervisión del transporte refrigerado.

#### 4.6. Exportación de información
Permite trabajar con registros en formato CSV y Excel, facilitando su revisión y análisis.
### 5. Modelo de Machine Learning

RutaFrío IA incorpora un modelo de aprendizaje supervisado para clasificar el nivel de riesgo del transporte refrigerado.

#### 5.1. Datos de entrenamiento

Se generó un conjunto de 500 viajes simulados con las siguientes variables:

- Distancia del viaje en kilómetros.
- Retraso del transporte en minutos.
- Tiempo de viaje en horas.
- Temperatura actual de la carga.
- Temperatura requerida.
- Desviación de temperatura.
- Nivel de riesgo: Bajo, Medio o Alto.

#### 5.2. Evaluación del modelo

El modelo fue evaluado utilizando 100 registros de prueba.

Resultados obtenidos:

- Exactitud general: 99 %.
- Riesgo Alto: F1-score de 1.00.
- Riesgo Medio: F1-score de 0.97.
- Riesgo Bajo: F1-score de 0.86.

El modelo obtuvo 99 predicciones correctas de 100 casos evaluados.

#### 5.3. Limitaciones

Los datos utilizados son sintéticos y fueron generados con fines educativos.

Por lo tanto, los resultados no constituyen una validación del modelo en condiciones reales de transporte.

Antes de utilizarlo en operaciones reales, sería necesario incorporar datos históricos, realizar pruebas adicionales y evaluar periódicamente su desempeño.
### 6. Tecnologías utilizadas

RutaFrío IA fue desarrollado utilizando las siguientes tecnologías:

- Python: lenguaje principal de programación.
- Streamlit: desarrollo de la interfaz interactiva.
- Pandas: procesamiento y análisis de datos.
- NumPy: operaciones numéricas y generación de datos.
- Scikit-learn: entrenamiento y evaluación del modelo de Machine Learning.
- Joblib: almacenamiento y recuperación del modelo entrenado.
- Requests: comunicación con servicios externos para el cálculo de rutas.
- Openpyxl: generación y lectura de archivos Excel.
- CSV: almacenamiento de registros de viajes y temperaturas.
- Visual Studio Code: entorno de desarrollo.

### 7. Entorno de desarrollo

El proyecto fue desarrollado en Windows, utilizando Visual Studio Code y un entorno virtual de Python denominado entorno_virtual.

El entorno virtual permite mantener organizadas las dependencias necesarias para ejecutar la aplicación.
### 8. Instalación y ejecución del proyecto

Para ejecutar RutaFrío IA en otro computador se requiere tener instalado Python.

#### 8.1. Preparar el entorno virtual

Abrir una terminal PowerShell en la carpeta del proyecto y ejecutar:

```powershell
python -m venv entorno_virtual
```

#### 8.2. Activar el entorno virtual

```powershell
.\entorno_virtual\Scripts\Activate.ps1
```

#### 8.3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

#### 8.4. Ejecutar la aplicación

```powershell
python -m streamlit run app.py
```

La aplicación se abrirá en el navegador, permitiendo utilizar las funcionalidades de RutaFrío IA.

Nota: Las funciones que dependen de servicios externos de rutas requieren conexión a Internet y la configuración correspondiente.
