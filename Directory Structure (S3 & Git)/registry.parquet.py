import mlflow
import dvc.api
import pandas as pd

# ---------------------------------------------------------
# 1. TRACKING THE EXPERIMENT (The "Why")
# ---------------------------------------------------------
def log_simulation_run(params, metrics, dvc_hash):
    """
    Links the Physics parameters to the Data Version.
    """
    with mlflow.start_run():
        # Log Physics Inputs
        mlflow.log_params(params)
        
        # Log Solver Convergence / Errors
        mlflow.log_metrics(metrics)
        
        # LINK MLFLOW TO DVC
        # This is the "Golden Thread" connecting Code, Config, and Data
        mlflow.set_tag("dvc.version", dvc_hash)
        mlflow.set_tag("data.path", "s3://my-bucket/silver/run_xyz.h5")

# ---------------------------------------------------------
# 2. QUERYING THE LAKEHOUSE (The "How")
# ---------------------------------------------------------
def get_training_data(min_velocity=50.0):
    """
    Acts like a SQL query on your file system.
    """
    # Load the lightweight registry (Sidecar)
    registry = pd.read_parquet("data/silver/registry.parquet")
    
    # Filter using Pandas (Fast for <10M runs)
    selected_runs = registry[registry['inlet_velocity'] > min_velocity]
    
    file_paths = selected_runs['s3_path'].tolist()
    
    return file_paths # Feed these into PyTorch DataLoader
