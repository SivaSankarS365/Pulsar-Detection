import sys
import numpy as np
from fastapi import FastAPI, File, UploadFile,Body, Request
import time
from typing import List
from io import BytesIO
import uvicorn
import os
import joblib
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from live_data_processing import preprocess_live_data

app = FastAPI(docs_url="/docs")

# Function to load the model from the specified path
def load_my_model(path: str):
    """
    Load the XGBoost model saved as a pickle file at the supplied path on the disk.

    Args:
    path (str): The path to the saved model on disk.

    Returns:
    xgboost.Booster: The loaded XGBoost model.

    Raises:
    ValueError: If the path is empty or does not exist.
    IOError: If there is an issue with reading the model file.
    """

    # Check if the path is empty
    if not path:
        raise ValueError("The path cannot be empty.")

    # Check if the file exists at the given path
    if not os.path.exists(path):
        raise ValueError(f"The file '{path}' does not exist.")

    # Check if the path is a file
    if not os.path.isfile(path):
        raise ValueError(f"'{path}' is not a file.")

    try:
        # Load the model using pickle
        with open(path, 'rb') as file:
            loaded_model = joblib.load(file)
        return loaded_model
    except IOError as e:
        raise IOError(f"Error reading model file: {e}")

@app.post("/predict")
async def predict_pulsar(request:Request,file: UploadFile = File(...),):
    """
    API Endpoint to predict whether a star is a pulsar or not.

    Args:
    file (UploadFile): The uploaded file.

    Returns:
    dict: A dictionary containing the predicted class (0 for not a pulsar and 1 for pulsar).
    """
 
    # Read the bytes from the uploaded image
        # Read the file content
    data = await file.read()
    df = pd.read_csv(BytesIO(data),header=None)

    input_data = np.array(df)[0]
    normalized_input_data = preprocess_live_data(input_data).reshape(1,-1)

    # Get the path to the model from the command line argument
    model_path = sys.argv[1]
    
    # Load the model
    loaded_model = load_my_model(model_path)
    # Predict the digit using the serialized array
    predicted_class = loaded_model.predict(normalized_input_data)
    # Return the predicted digit to the client
    return {"Class": str(predicted_class)}

if __name__ == "__main__":

    # Check if the path to the model is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python api-app.py <path_to_model>")
        sys.exit(1)
    
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=5000)