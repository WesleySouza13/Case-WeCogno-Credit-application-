from pathlib import Path
import mlflow.sklearn

def model_predict(X):
    project_path = Path(__file__).resolve().parent.parent
    model_path = project_path / "artifacts" / "modelo_para_producao"
    if not model_path.is_dir():
        raise FileNotFoundError(
            f"Modelo não encontrado: {model_path}")
    model = mlflow.sklearn.load_model(str(model_path))
    return model.predict_proba(X)[:, 1]

