# Proyecto MLOps con Jupyter, MLflow, PostgreSQL y Docker

## 📌 Descripción
Este proyecto implementa un flujo de trabajo de **MLOps** donde se entrena un modelo de Machine Learning utilizando **Jupyter Notebook**, se registran los experimentos en **MLflow**, y se almacenan los resultados en **PostgreSQL**. Todo se despliega utilizando **Docker**.

## 📁 Estructura del Proyecto
```
├── docker-compose.yml  # Configuración de servicios Docker
├── Dockerfile          # Imagen de Jupyter con dependencias
├── notebooks/          # Notebooks de entrenamiento y pruebas
├── mlflow-server/      # Configuración del servidor MLflow
├── database/           # Scripts de base de datos PostgreSQL
├── README.md           # Documentación del proyecto
```

## 🚀 Requisitos Previos
Antes de ejecutar este proyecto, asegúrate de tener instalado:
- **Docker** y **Docker Compose**
- **Python 3.x**
- **JupyterLab**
- **MLflow**
- **PostgreSQL**

## ⚙️ Instalación y Configuración

### 1️⃣ **Configurar y ejecutar Docker**
Ejecuta el siguiente comando para construir y levantar los contenedores:
```sh
docker-compose up --build
```
Esto iniciará los siguientes servicios:
- **JupyterLab** en `http://localhost:8888`
- **MLflow Tracking Server** en `http://localhost:5000`
- **PostgreSQL** en `localhost:5432`

### 2️⃣ **Conectar MLflow con el Servidor Externo**
Si el servidor MLflow está en una máquina remota (`ip:puerto`), configura la conexión en Jupyter:
```python
import mlflow
mlflow.set_tracking_uri("http://ip:puerto")
print("MLflow Tracking URI configurado ✅")
```

### 3️⃣ **Conectar PostgreSQL con Jupyter**
Para registrar los resultados en la base de datos, primero establecemos una conexión:
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mlops_db",
    user="mlops_user",
    password="mlops_password",
    port=5432
)
cursor = conn.cursor()
print("Conexión a PostgreSQL establecida ✅")
```

### 4️⃣ **Entrenar y Registrar un Modelo**
En un notebook de Jupyter, ejecuta (Ejemplo):
```python
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
import numpy as np

modelo = LinearRegression()
modelo.fit(X, y)

with mlflow.start_run():
    mlflow.log_param("alpha", 0.01)
    mlflow.log_metric("mse", 0.025)
    mlflow.sklearn.log_model(modelo, artifact_path="model", registered_model_name="Modelo_ML")
```

### 5️⃣ **Guardar Resultados en PostgreSQL**
```python
cursor.execute("""
    INSERT INTO experiment_results (experiment_name, metric, value)
    VALUES ('Modelo_ML', 'mse', 0.025);
""")
conn.commit()
print("Resultados guardados en PostgreSQL ✅")
```

## 📊 Visualización de Resultados
Puedes consultar los modelos registrados en MLflow desde la UI:
```sh
mlflow ui --host 0.0.0.0 --port 5000
```
Y los resultados en PostgreSQL con:
```sh
docker exec -it postgres_container psql -U mlops_user -d mlops_db -c "SELECT * FROM experiment_results;"
```


## 📌 Conclusión
Este proyecto demuestra cómo usar **MLOps** con **Docker, MLflow, PostgreSQL y Jupyter** para entrenar modelos, registrar experimentos y almacenar resultados en una base de datos. 🚀

