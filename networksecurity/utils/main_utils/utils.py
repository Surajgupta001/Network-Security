import os
import sys
import numpy as np
import pickle
from sklearn.metrics import r2_score
import yaml

from sklearn.model_selection import GridSearchCV

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        logging.info(f"Reading YAML file from: {file_path}")
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        logging.info(f"Writing YAML file to: {file_path}")
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w") as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.ndarray):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        logging.info(f"Saving numpy array to file: {file_path}")
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info(f"Saving object to file: {file_path}")
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        logging.info(f"Loading object from file: {file_path}")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    Load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        logging.info(f"Loading numpy array from file: {file_path}")
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def evaluate_models(
    X_train, Y_train, X_test, Y_test, models: dict, params: dict
) -> dict:
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, Y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, Y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(Y_train, y_train_pred)
            test_model_score = r2_score(Y_test, y_test_pred)

            logging.info(
                f"Evaluated model {list(models.keys())[i]} with train score {train_model_score} and test score {test_model_score}"
            )

            report[list(models.keys())[i]] = test_model_score

        logging.info(f"Model evaluation report generated: {report}")
        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
