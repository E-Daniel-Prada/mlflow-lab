import os
import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar la URL de MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://10.43.101.184:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()

#Obtiene el ultimo modelo resgistrado
def get_latest_model():
    """
    Obtiene el nombre del último modelo registrado en MLflow.
    :return: Nombre del modelo o None si no hay modelos registrados.
    """
    try:
        models = client.search_registered_models()
        if models:
            return models[-1].name  # Último modelo agregado en MLflow
        return None
    except Exception as e:
        print(f"⚠️ Error al obtener modelos de MLflow: {e}")
        return None

#Carga de modelo
def load_model():
    """
    Carga automáticamente el modelo más reciente disponible en MLflow.
    :return: Modelo de MLflow si existe, de lo contrario None.
    """
    model_name = get_latest_model()
    if not model_name:
        print("⚠️ No hay modelos disponibles en MLflow.")
        return None

    print(f"✅ Cargando modelo: {model_name}")
    model_uri = f"models:/{model_name}/latest"
    try:
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        print(f"⚠️ Error al cargar el modelo: {e}")
        return None

#Realiza la prediccion
def make_prediction(model, input_data):
    """
    Realiza una predicción con el modelo cargado.
    :param model: Modelo de MLflow cargado.
    :param input_data: Datos de entrada en formato JSON.
    :return: Resultado de la inferencia.
    """
    if model is None:
        return {"error": "No hay modelos disponibles para hacer inferencias."}
    
    prediction = model.predict(input_data)
    return {"prediction": prediction.tolist()}

#Obtener Detalles de un experimiento especifico
def get_experiment_details(experiment_name):
    """
    Devuelve detalles de un experimento en MLflow.

    :param experiment_name: Nombre del experimento.
    :return: Detalles del experimento o error si no existe.
    """
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment:
        return {
            "experiment_id": experiment.experiment_id,
            "artifact_location": experiment.artifact_location,
            "lifecycle_stage": experiment.lifecycle_stage
        }
    return {"error": "Experiment not found"}

#Obtener detaller de un run especifico
def get_run_details(run_id):
    """
    Devuelve detalles de un run en MLflow.

    :param run_id: ID del run a consultar.
    :return: Diccionario con detalles del run.
    """
    try:
        run = client.get_run(run_id)
        return {
            "run_id": run.info.run_id,
            "experiment_id": run.info.experiment_id,
            "status": run.info.status,
            "start_time": run.info.start_time,
            "end_time": run.info.end_time,
            "params": run.data.params,
            "metrics": run.data.metrics
        }
    except Exception as e:
        return {"error": str(e)}