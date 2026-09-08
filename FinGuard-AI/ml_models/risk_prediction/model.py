"""Risk Prediction Model using XGBoost"""

import numpy as np
import xgboost as xgb
import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class RiskPredictor:
    """XGBoost-based risk prediction for late payment"""

    def __init__(self, model_path: str = "models/risk_predictor.pkl"):
        self.model_path = Path(model_path)
        self.model = None
        self.is_trained = False

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train risk prediction model"""
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            verbosity=0,
        )
        self.model.fit(X, y)
        self.is_trained = True
        logger.info(f"Risk predictor trained on {X.shape[0]} samples")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict late payment risk probability"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        predictions = self.model.predict(X)
        return np.clip(predictions, 0, 1)

    def predict_single(self, features: list) -> float:
        """Predict single invoice risk"""
        X = np.array([features]).reshape(1, -1)
        risk = self.predict(X)
        return float(risk[0])

    def save(self) -> None:
        """Save model to disk"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        logger.info(f"Risk predictor saved to {self.model_path}")

    def load(self) -> None:
        """Load model from disk"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        self.model = joblib.load(self.model_path)
        self.is_trained = True
        logger.info(f"Risk predictor loaded from {self.model_path}")


risk_predictor = RiskPredictor()
