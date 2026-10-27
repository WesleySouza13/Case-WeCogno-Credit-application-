# %% 
from pathlib import Path
import mlflow
import mlflow.sklearn

project_path = Path.cwd()
db_path = project_path / "mlflow" / "mlflow.db"

db_uri = f"sqlite:///{db_path.as_posix()}"

mlflow.set_tracking_uri(db_uri)
mlflow.set_registry_uri(db_uri)

# Carrega o modelo registrado
model = mlflow.sklearn.load_model(
    "models:/modelo_para_producao@champion"
)

# Salva o modelo dentro do projeto
model_path = project_path / "artifacts" / "modelo_para_producao"

mlflow.sklearn.save_model(
    sk_model=model,
    path=str(model_path),
    serialization_format="cloudpickle"
)

print(f"Modelo salvo em: {model_path}")
# %%
