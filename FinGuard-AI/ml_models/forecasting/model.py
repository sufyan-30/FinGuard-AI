"""Financial Forecasting Model using ARIMA/Prophet"""

import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Forecaster:
    """Simple forecasting model for payment trends"""

    def __init__(self, model_path: str = "models/forecaster.pkl"):
        self.model_path = Path(model_path)
        self.model = None
        self.is_trained = False

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train forecasting model"""
        self.model = LinearRegression()
        self.model.fit(X, y)
        self.is_trained = True
        logger.info(f"Forecaster trained on {X.shape[0]} samples")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Forecast payment amounts"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        return self.model.predict(X)

    def predict_single(self, features: list) -> float:
        """Predict single forecast"""
        X = np.array([features]).reshape(1, -1)
        forecast = self.predict(X)
        return float(forecast[0])

    def save(self) -> None:
        """Save model to disk"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        logger.info(f"Forecaster saved to {self.model_path}")

    def load(self) -> None:
        """Load model from disk"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        self.model = joblib.load(self.model_path)
        self.is_trained = True
        logger.info(f"Forecaster loaded from {self.model_path}")


forecaster = Forecaster()
