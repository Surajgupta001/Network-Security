import sys
import os
import pymongo

import pandas as pd
from dotenv import load_dotenv

import certifi

from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse


ca = certifi.where()
load_dotenv()

mongo_db_url = os.getenv("MONGODB_URI")
logging.info(f"MongoDB URL: {mongo_db_url}")

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(
            content="Training completed successfully", media_type="text/plain"
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        app_run(app, host="localhost", port=8000)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
