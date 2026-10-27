# %%
import mlflow
import os
from pathlib import Path
import pandas as pd 

def model_predict(X:pd.DataFrame):
    project_path = Path(__file__).resolve().parent.parent
    db_path = project_path / "mlflow" / "mlflow.db"
    db_uri = db_path.as_posix()
    mlflow.set_tracking_uri(f"sqlite:///{db_uri}")
    mlflow.set_registry_uri(f"sqlite:///{db_uri}")
    model = mlflow.sklearn.load_model("models:/modelo_para_producao@champion")

    return model.predict_proba(X)[:, 1]
# %%
