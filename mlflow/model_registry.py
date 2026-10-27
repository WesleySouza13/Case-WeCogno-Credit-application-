# %% 
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
import joblib 
import os 

model_path = os.path.join('..',  'XGBoost.pkl')
model = joblib.load(model_path)
# %%
with mlflow.start_run() as run:
    mlflow.sklearn.log_model(sk_model=model, name='XGBoost_optunado_calibrado', 
                            registered_model_name='modelo_para_producao', serialization_format='cloudpickle')

# %%
client = MlflowClient()
client.set_registered_model_alias(name='modelo_para_producao',alias='champion',version=7)
print("Run ID:", run.info.run_id)
# %%
versions = client.search_model_versions(
    "name='modelo_para_producao'"
)
# %%
print(client.search_registered_models())
# %%
project_path = r"C:\Users\souza\OneDrive\Área de Trabalho\case1_wecogno"
db_path = os.path.join(project_path,"predict","mlflow.db")

if not os.path.exists(db_path):
    raise FileNotFoundError(f"Banco não encontrado: {db_path}")

db_uri = "sqlite:///" + db_path.replace("\\", "/")

mlflow.set_tracking_uri(db_uri)
mlflow.set_registry_uri(db_uri)
print("Banco:", db_path)
print("Tracking URI:", mlflow.get_tracking_uri())
# %%
