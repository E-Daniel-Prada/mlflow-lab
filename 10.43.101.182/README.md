# 🚀 MLflow API - Inferencia y Gestión de Modelos

Este proyecto implementa una API basada en **FastAPI** para la gestión y consumo de modelos de Machine Learning utilizando **MLflow**. Permite realizar inferencias con modelos registrados, consultar experimentos y gestionar modelos en un entorno de despliegue.

---

## 📂 Estructura del Proyecto

```
mlflow-api/
│── Dockerfile                   # Configuración de la imagen Docker
│── docker-compose.yml           # Orquestación de servicios en Docker
│── requirements.txt             # Dependencias necesarias para la API
│── .env                         # Variables de entorno
│── app/                         # Código de la API
│   ├── main.py                  # Código principal de la API (FastAPI)
│   ├── inference.py             # Lógica de inferencia y carga de modelos
│   ├── __init__.py              # Archivo de inicialización del módulo
```

---

## 📌 **Funcionalidades de la API**

✅ **Carga automática de modelos registrados en MLflow**  
✅ **Realización de predicciones con los modelos disponibles**  
✅ **Consulta de experimentos registrados en MLflow**  
✅ **Gestión de modelos para selección del más reciente**  
✅ **Despliegue con Docker y Docker Compose**  

---

## 🔧 **Instalación y Configuración**

### 1️⃣ **Pre-requisitos**
- Docker
- Docker Compose
- Python 3.10 o superior (si se ejecuta fuera de Docker)

### 2️⃣ **Configuración del entorno**
El archivo `.env` debe contener la URL del servidor MLflow:
```env
MLFLOW_TRACKING_URI=http://10.43.101.184:5000
```

---

## 🚀 **Despliegue de la API con Docker**

### 🔹 **1️⃣ Construir y ejecutar los contenedores**
```bash
sudo docker-compose up -d --build
```

### 🔹 **2️⃣ Verificar los logs del servicio**
```bash
docker logs mlflow_api
```

### 🔹 **3️⃣ Verificar que la API esté corriendo**
```bash
curl -X 'GET' 'http://localhost:8888'
```
Salida esperada:
```json
{"message": "API de Inferencia y Experimentos con MLflow está corriendo"}
```

---

## 🔍 **Endpoints Disponibles**

### 🔹 **1️⃣ Listar Modelos Registrados**
```bash
curl -X 'GET' 'http://localhost:8888/models'
```
📌 **Respuesta esperada:**
```json
{"models": ["random_forest_model"]}
```

### 🔹 **2️⃣ Realizar una Predicción**
```bash
curl -X 'POST' 'http://localhost:8888/predict/' \
  -H 'Content-Type: application/json' \
  -d '{"features": [3305, 35, 13, 134, 25, 5811, 218, 211, 127, 659, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]}'
```
📌 **Respuesta esperada:**
```json
{"prediction": [2]}
```

### 🔹 **3️⃣ Obtener Información de un Experimento**
```bash
curl -X 'GET' 'http://localhost:8888/experiment/random_forest_model'
```

### 🔹 **4️⃣ Obtener Información de una Ejecución en MLflow**
```bash
curl -X 'GET' 'http://localhost:8888/run/{run_id}'
```

---

## 🔍 **Funcionamiento Interno**

### 📌 **Carga Automática del Último Modelo en MLflow**
El sistema detecta automáticamente el modelo más reciente en MLflow y lo carga en memoria:
```python
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
client = MlflowClient()
model_uri = f"models:/{model_name}/latest"
model = mlflow.pyfunc.load_model(model_uri)
```

### 📌 **Inferencia con el Modelo**
El endpoint `/predict/` recibe datos en formato JSON y realiza la predicción con el modelo cargado:
```python
def make_prediction(model, input_data):
    if model is None:
        return {"error": "No hay modelos disponibles para hacer inferencias."}
    prediction = model.predict(input_data)
    return {"prediction": prediction.tolist()}
```

---

## 🎯 **Conclusión**
Este proyecto permite la integración con **MLflow** para la gestión y consumo de modelos de Machine Learning, facilitando el despliegue y uso de modelos en producción mediante una API accesible. 🚀


