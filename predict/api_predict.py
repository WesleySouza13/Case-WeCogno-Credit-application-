# %%
import mlflow
from pathlib import Path
import pandas as pd 

def model_predict(X:pd.DataFrame):
    project_path = Path(__file__).resolve().parent.parent
    db_path = project_path / "mlflow" / "mlflow.db"
    if not db_path.is_file():
        raise FileNotFoundError(f"Banco do MLflow não encontrado: {db_path}")
    db_uri = f"sqlite:///{db_path.as_posix()}"
    mlflow.set_tracking_uri(db_uri)
    mlflow.set_registry_uri(db_uri)
    model = mlflow.sklearn.load_model("models:/modelo_para_producao@champion")

    return model.predict_proba(X)[:, 1]
# %%
