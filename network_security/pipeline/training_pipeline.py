import os, sys

from network_security.cloud.s3_syncer import S3Sync
from network_security.exception.exceptions import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.constants.training_pipeline import TRAINING_BUCKET_NAME

from network_security.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig,
)

from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifacts,
    ModelTrainerArtifact
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config= TrainingPipelineConfig()
        self.s3_sync = S3Sync()
        
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Ingestion pipeline started")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            logging.info("Data Ingestion pipeline Completed")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config= DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation= DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info("Data validation pipeline started")
            data_validation_artifacts=data_validation.initiate_data_validation()
            logging.info("Data validation pipeline Completed")
            return data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact: DataValidationArtifacts):
        try:
            data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data transformation pipeline started")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
            data_transformation_artifacts= data_transformation.initiate_data_transformation()
            logging.info("Data transformation pipeline completed")
            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_training(self,data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info("Model Training Pipeline Started")
            self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info(" Model training Artifacts created")
            return model_trainer_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    ## upload artifacts from local to S3 bucket    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    ## upload final model from local to S3 bucket 
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


    def run_pipeline(Self):
        try:
            data_ingestion_artifact=Self.start_data_ingestion()
            data_validation_artifact= Self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=Self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_training_artifact=Self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            
            Self.sync_artifact_dir_to_s3()
            Self.sync_saved_model_dir_to_s3()
            
            return model_training_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        