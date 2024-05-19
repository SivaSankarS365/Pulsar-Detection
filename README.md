# Pulsar Detection Project, BDL-Project

## Problem

Pulsars are a type of neutron star that emit beams of electromagnetic radiation. Detecting pulsars is a significant challenge in the field of astronomy due to their sparse occurrence and the presence of a vast amount of noise in the data. Efficiently processing and analyzing large datasets to identify these celestial objects requires robust data processing and machine learning techniques.

## File Structure

This project is organized into several key directories and files to facilitate data acquisition, processing, and modeling.

```bash
PulsarDetectionProject/
├── download/
│   ├── fetch_data_dag.py     # Airflow DAG to fetch the latest data
│   ├── data/                 # Directory where the fetched data will be stored
├── modeling/
│   ├── train_model.py        # Script for training models to predict pulsars using MLflow
│   ├── models/               # Directory to save trained models
├── pulsar_processing.py      # Data processing script using Apache Beam
├── requirements.txt          # Required Python packages
├── README.md                 # Project documentation
```


### Detailed Descriptions

#### download/

This directory contains the Airflow DAG script `pulsar_data_download.py` which automates the process of downloading the latest pulsar data. The downloaded data is stored in the `data/` subdirectory.

**Files:**

- dags/pulsar_data_download `.py `: An Airflow DAG to schedule and automate data fetching tasks.

**Usage:**

1. Ensure Airflow is properly installed and configured.
2. Place the `pulsar_data_download.py` script in the Airflow DAGs directory.
3. Start the Airflow scheduler to begin fetching data periodically.

#### modeling/

This directory is dedicated to building and training machine learning models to predict pulsars. The main script `getmodel_mlflow.py` utilizes MLflow for tracking experiments and model management.

**Files:**

- getmodel_mlflow `.py `: A script to train various machine learning models for pulsar detection.
- `models/`: A directory to store trained models.

**Usage:**

1. Ensure MLflow is installed and configured.
2. Run the getmodel_mlflow `.py ` script to start training models.
3. Use MLflow UI to track and manage experiments.

#### pulsar_processing.py

This standalone script is responsible for data processing using Apache Beam. It reads the raw pulsar data, performs cleaning, feature engineering, and prepares the data for modeling.

**Usage:**

1. Ensure Apache Beam is installed.
2. Run the `pulsar_processing.py` script to process the data.

   ```sh
   python pulsar_processing.py
   ```
