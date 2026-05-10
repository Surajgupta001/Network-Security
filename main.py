import sys

from networksecurity import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
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
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config,
        )
        logging.info("Starting data validation")
        data_validation_artifact = data_validation.initialize_data_validation()
        logging.info("Data validation completed successfully")
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
