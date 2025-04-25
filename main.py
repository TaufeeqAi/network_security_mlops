from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exceptions import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer

import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Data Ingestion pipeline started")
        dataingestionartifact= data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion pipeline Completed")
        print(dataingestionartifact)
        
        data_validation_config= DataValidationConfig(trainingpipelineconfig)
        data_validation= DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Data validation pipeline started")
        data_validation_artifacts=data_validation.initiate_data_validation()
        logging.info("Data validation pipeline Completed")
        print(data_validation_artifacts)

        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info("Data transformation pipeline started")
        data_transformation = DataTransformation(data_validation_artifacts,data_transformation_config)
        data_transformation_artifacts= data_transformation.initiate_data_transformation()
        logging.info("Data transformation pipeline completed")
        print(data_transformation_artifacts)

        logging.info("Model Training Pipeline Started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifacts)
        model_trainer_artifacts = model_trainer.initiate_model_trainer()
        logging.info(" Model training Artifacts created")
        print(model_trainer_artifacts)


    except Exception as e:
        raise NetworkSecurityException(e,sys)