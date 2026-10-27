# %%
import mlflow
import os
from pathlib import Path
import pandas as pd 

def model_predict(X:pd.DataFrame):
    project_path = Path(os.environ["PATCH_case1"])
    db_path = os.path.join(project_path, "mlflow", "mlflow.db")
    db_uri = "sqlite:///" + db_path.replace("\\", "/")
    mlflow.set_tracking_uri(db_uri)
    mlflow.set_registry_uri(db_uri)
    model = mlflow.sklearn.load_model("models:/modelo_para_producao@champion")
    return model.predict_proba(X)[:,1]
# %%
