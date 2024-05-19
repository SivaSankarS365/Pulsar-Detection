import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import mlflow
import mlflow.xgboost
from sklearn.model_selection import ParameterSampler
import joblib


mlflow.set_tracking_uri("http://127.0.0.1:8080")

# Load the dataset
dataset = "HTRU_2_processed.csv-00000-of-00001"
df = pd.read_csv(dataset, header=None)

# Separate features and target
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Define the hyperparameter space
param_distributions = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0]
}

# Number of random samples
n_iter_search = 10

# Generate random parameter combinations
random_search = ParameterSampler(param_distributions, n_iter=n_iter_search, random_state=42)

# Start MLflow experiment
mlflow.set_experiment("Pulsar_Classification_XGBoost")

best_accuracy = 0
best_run_id = None
best_model_params = None

for idx, params in enumerate(random_search):
    with mlflow.start_run(run_name=f"run_{idx}") as run:
        # Log hyperparameters
        mlflow.log_params(params)

        # Initialize and train the XGBoost model with the current set of hyperparameters
        model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', **params)
        model.fit(X_train, y_train)

        # Predict on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, output_dict=True)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", class_report['weighted avg']['precision'])
        mlflow.log_metric("recall", class_report['weighted avg']['recall'])
        mlflow.log_metric("f1-score", class_report['weighted avg']['f1-score'])

        # Log the confusion matrix as an artifact
        conf_matrix_df = pd.DataFrame(conf_matrix)
        conf_matrix_df.to_csv("confusion_matrix.csv", index=False)
        mlflow.log_artifact("confusion_matrix.csv")
        
        # Check if this is the best model so far
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_run_id = run.info.run_id
            best_model_params = params

# Save the best model locally
if best_run_id is not None:
    print(f"Best model found in run {best_run_id} with accuracy {best_accuracy}")
    best_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', **best_model_params)
    best_model.fit(X_train, y_train)
    
    # Save the model to a file
    model_filename = "best_xgboost_model.pkl"
    joblib.dump(best_model, model_filename)
    print(f"Best model saved to {model_filename}")

print("Experiment completed and best model saved locally.")


