import os
from fastapi import FastAPI
from pydantic import BaseModel
from app.inference import load_model, make_prediction, get_experiment_details, get_run_details
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = FastAPI()

# Obtener la URL de MLflow desde .env
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://10.43.101.184:5000")

# Crear cliente de MLflow
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

# Cargar automáticamente el último modelo disponible en MLflow
model = load_model()

class InputData(BaseModel):
    """Formato de entrada para la inferencia."""
    features: list  # Lista de valores para la predicción

@app.get("/")
def home():
    return {"message": "API de Inferencia y Experimentos con MLflow está corriendo"}

@app.post("/predict/")
def predict(data: InputData):
    """Realiza una predicción solo si el modelo está disponible."""
    return make_prediction(model, [data.features])

@app.get("/experiment/{experiment_name}")
def experiment_info(experiment_name: str):
    """Devuelve información de un experimento en MLflow."""
    return get_experiment_details(experiment_name)

@app.get("/run/{run_id}")
def run_info(run_id: str):
    """Devuelve detalles de un run en MLflow."""
    return get_run_details(run_id)

@app.get("/models")
def list_models():
    """Lista los modelos disponibles en MLflow con manejo de errores."""
    try:
        models = [m.name for m in client.search_registered_models()]
        if not models:
            return {"message": "No hay modelos registrados en MLflow"}
        return {"models": models}
    except Exception as e:
        return {"error": str(e)}
