import logging
import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    TrainingPipelineConfig,
)
from networksecurity.exception.exception import NetworkSecurityException


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("Starting data ingestion")

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed successfully")
        print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
