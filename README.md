# Pulsar Detection Project
<p align="center">
   <img width="333" alt="image" src="https://github.com/user-attachments/assets/1a0bb452-48ad-4c2a-8203-526251816d1e">

</p>


## Overview

Pulsars are rapidly rotating neutron stars that emit beams of electromagnetic radiation. Detecting these celestial objects is challenging due to their rarity and the overwhelming noise in astronomical data. This project leverages advanced data processing and machine learning techniques to identify pulsars from large datasets efficiently.

## Purpose

This project aims to showcase the application of MLOps tools in a typical industrial project workflow. By integrating tools like MLflow, Apache Beam, Apache Airflow, and Prometheus, this project demonstrates how to streamline and automate the end-to-end process of data acquisition, model training, deployment, and monitoring. This approach ensures scalability, reproducibility, and efficient management of machine learning models in real-world scenarios.

## Deployment

To deploy the Pulsar Detection Project, you can either use Docker for containerization or run the application directly on your machine.

### Clone the Repository

```bash
git clone https://github.com/SivaSankarS365/Pulsar-Detection.git
```

### Without Docker

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the FastAPI application:
   ```bash
   python deploy/api-app.py modeling/best_xgboost_model.pkl
   ```

### With Docker

1. Build the Docker image:
   ```bash
   docker build -t pulsar-fastapi-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 -p 18000:18000 pulsar-fastapi-app
   ```

### Monitoring

You can monitor the application using Prometheus and Node Exporter:

1. Start Node Exporter:
   ```bash
   ./node_exporter --web.listen-address=:9200 &
   ```

2. Start Prometheus with the specified configuration:
   ```bash
   "$PATHTOPROMETHEUSBINARY$" --config.file=deploy/prometheus.yml
   ```

## Problem Statement

Pulsars are challenging to detect due to their sparse occurrence and the vast amount of noise in the data. This project addresses this challenge by applying robust data processing and machine learning techniques to analyze large datasets and accurately identify pulsars.

## Project Structure
<img width="829" alt="image" src="https://github.com/user-attachments/assets/dcf66dcc-54c9-4c77-8047-78ecd7e84b05">
```bash
PulsarDetectionProject/
├── deploy/
│   └── api-app.py
├── download/
│   ├── fetch_data_dag.py
│   └── data/
├── modeling/
│   ├── train_model.py
│   └── models/
├── pulsar_processing.py
├── requirements.txt
└── README.md
```

### Directory and File Descriptions

#### `deploy/`

- **`api-app.py`**: Contains the FastAPI application code for deploying the pulsar detection service.

#### `download/`

- **`fetch_data_dag.py`**: An Airflow DAG that automates downloading the latest pulsar data. The data is stored in the `data/` subdirectory.

**Usage:**

1. Place `fetch_data_dag.py` in the Airflow DAGs directory.
2. Start the Airflow scheduler to fetch data periodically.

#### `modeling/`

- **`train_model.py`**: Script to train machine learning models for pulsar detection using MLflow for experiment tracking.
- **`models/`**: Directory to store the trained models.

**Usage:**

1. Run `train_model.py` to start training.
2. Use MLflow UI to track and manage experiments.

#### `pulsar_processing.py`

This script processes the raw pulsar data using Apache Beam, performing data cleaning, feature engineering, and preparation for modeling.

**Usage:**

1. Ensure Apache Beam is installed.
2. Run the script:
   ```bash
   python pulsar_processing.py
   ```

## Tools Used

### MLflow

MLflow is an open-source platform for managing the machine learning lifecycle, including experimentation, reproducibility, and deployment. In this project, MLflow is used to track the performance of various models and efficiently manage the trained models.

### Apache Beam

Apache Beam is a unified programming model for defining and executing data processing pipelines. It is utilized in this project for scalable and efficient processing of large pulsar datasets.

### Apache Airflow

Apache Airflow is an open-source tool for programmatically authoring, scheduling, and monitoring workflows. In this project, Airflow automates the data fetching process, ensuring that the models are always trained on the most recent data.

### Prometheus

Prometheus is an open-source systems monitoring and alerting toolkit. In this project, Prometheus is used to monitor the application and infrastructure, providing real-time metrics and insights to ensure the system's health and performance.

## Conclusion

This project combines cutting-edge machine learning, data processing, and workflow automation tools to address the challenge of detecting pulsars in noisy astronomical data. By leveraging Docker for deployment and tools like MLflow, Apache Beam, and Airflow, we ensure that the project is scalable, reproducible, and easy to maintain.
