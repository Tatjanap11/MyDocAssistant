import mlflow

def set_mlflow_logging(experiment_name):
    # Check if the experiment already exists
    existing_experiment = mlflow.get_experiment_by_name(experiment_name)

    if existing_experiment:
        print(f"Experiment '{experiment_name}' already exists with ID {existing_experiment.experiment_id}.")
        mlflow.set_experiment(experiment_name)
    else:
        # Create the experiment if it doesn't exist
        experiment_id = mlflow.create_experiment(experiment_name)
        print(f"Experiment '{experiment_name}' created with ID {experiment_id}.")
        mlflow.set_experiment(experiment_name)