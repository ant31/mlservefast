from mlflow import pyfunc

def get_model(model_path: str):
    model = pyfunc.load_model(model_path)
