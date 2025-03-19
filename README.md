# 📌 Proyecto MLOps con MLflow, MinIO, Jupyter y API

Este proyecto implementa un **flujo de trabajo de MLOps** distribuido en tres máquinas que colaboran para entrenar, registrar y servir modelos de Machine Learning utilizando **MLflow, MinIO, Jupyter y FastAPI**.

---

## 📌 Arquitectura del Proyecto

El proyecto se distribuye en tres máquinas:

![arquitectura_mlflow](https://github.com/user-attachments/assets/2b964b7c-8df3-4e46-ad79-d4c9fa5b2504)

| Máquina             | IP               | Componentes Instalados |
|--------------------|-----------------|------------------------|
| **Servidor MLflow** | `10.43.101.184`  | MLflow Server, MinIO, PostgreSQL |
| **Entrenamiento ML** | `10.43.101.191`  | Jupyter Notebook, PostgreSQL |
| **API de Inferencia** | `10.43.101.182`  | API con FastAPI y MLflow |

---

## 📂 Estructura del Proyecto

```
mlflow-lab-main/
├── 10.43.101.184/           # Servidor MLflow + MinIO
│   ├── docker-compose.yml   # Configuración de contenedores
│   ├── mlflow_serv.service  # Servicio de MLflow en systemctl
│   ├── minio/               # Almacenamiento de artefactos
│   ├── README.md            # Documentación del servidor
│
├── 10.43.101.191/           # Jupyter Notebook + Model Training
│   ├── Dockerfile           # Imagen Docker de Jupyter
│   ├── notebooks/           # Notebooks de entrenamiento
│   ├── train_preprocessed.csv  # Datos de entrenamiento
│   ├── README.md            # Documentación del entrenamiento
│
├── 10.43.101.182/           # API de Inferencia
│   ├── mlflow-api/          # Código de la API FastAPI
│   ├── Dockerfile           # Imagen Docker de la API
│   ├── docker-compose.yml   # Configuración de servicios
│   ├── app/                 # Código de la API
│   │   ├── main.py          # API principal en FastAPI
│   │   ├── inference.py     # Lógica de predicción con MLflow
│   ├── README.md            # Documentación de la API
│
├── images/                  # Recursos gráficos
│   ├── arquitectura_mlflow.jpg
│
├── .gitignore               # Archivos a ignorar
├── README.md                # Este archivo
```

---

## 🚀 Cómo Ejecutar el Proyecto

Cada máquina tiene su propio entorno. Para ejecutarlo, sigue estos pasos:

### **1️⃣ Servidor MLflow (10.43.101.184)**
#### 🔹 **Ejecutar los servicios**
```sh
cd 10.43.101.184
docker-compose up -d
```
Esto iniciará:
- **MLflow Tracking Server** en `http://10.43.101.184:5000`
- **MinIO** para almacenamiento en `http://10.43.101.184:9000`

---

### **2️⃣ Máquina de Entrenamiento (10.43.101.191)**
#### 🔹 **Ejecutar Jupyter Notebook**
```sh
cd 10.43.101.191
docker-compose up -d
```
Acceder a Jupyter Notebook en:  
👉 `http://10.43.101.191:8888`

#### 🔹 **Ejecutar un entrenamiento en Jupyter**
```python
import mlflow
mlflow.set_tracking_uri("http://10.43.101.184:5000")

# Entrenar y registrar modelo en MLflow
mlflow.sklearn.log_model(model, artifact_path="random_forest_model", registered_model_name="RandomForest")
```

---

### **3️⃣ API de Inferencia (10.43.101.182)**
#### 🔹 **Levantar la API**
```sh
cd 10.43.101.182/mlflow-api
docker-compose up -d
```
La API estará disponible en:  
👉 `http://10.43.101.182:8000/docs`

#### 🔹 **Hacer una Predicción**
```sh
curl -X POST "http://10.43.101.182:8000/predict"      -H "Content-Type: application/json"      -d '{"features": [1.2, 3.4, 5.6, 7.8]}'
```

---

## 📌 Endpoints de la API

| Método | Endpoint        | Descripción |
|--------|----------------|-------------|
| **GET**  | `/models`      | Lista los modelos registrados en MLflow |
| **POST** | `/predict`     | Realiza una predicción con el modelo más reciente |
| **GET**  | `/experiments` | Muestra los experimentos en MLflow |

---

## 🔥 Conclusión

Este proyecto demuestra cómo implementar **MLOps** con un enfoque distribuido, permitiendo:
✔ Registro de experimentos con **MLflow**  
✔ Almacenamiento eficiente de modelos en **MinIO**  
✔ Entrenamiento y pruebas en **Jupyter Notebook**  
✔ Inferencia en tiempo real con **FastAPI**  

---

¡Listo para presentar al profesor! 🚀  
Si necesitas ajustes, dime qué agregar. 😃
