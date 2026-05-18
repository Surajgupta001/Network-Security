import sys
import os
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimated import NetworkModel
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
from fastapi.templating import Jinja2Templates


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

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
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


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor_path = os.path.join("final_model", "preprocessor.pkl")
        model_path = os.path.join("final_model", "model.pkl")

        if not os.path.exists(preprocessor_path) or not os.path.exists(model_path):
            logging.error(
                f"Model artifacts missing. Expected: {preprocessor_path}, {model_path}"
            )
            raise Exception("Model artifacts not found. Please run training first.")

        preprocessor = load_object(preprocessor_path)
        final_model = load_object(model_path)
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        logging.info(f"Received data for prediction: {df.shape}")
        y_read = network_model.predict(df)
        df["predicted_column"] = y_read

        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv(os.path.join("prediction_output", "output.csv"), index=False)

        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse(
            "table.html", {"request": request, "table": table_html}
        )
    except Exception as e:
        logging.exception("Prediction failed")
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        app_run(app, host="localhost", port=8000)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
