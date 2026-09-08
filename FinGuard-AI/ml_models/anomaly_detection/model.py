"""Anomaly Detection Model using Isolation Forest"""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Isolation Forest-based anomaly detection for invoices"""

    def __init__(self, model_path: str = "models/anomaly_detector.pkl"):
        self.model_path = Path(model_path)
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False

    def train(self, X: np.ndarray, contamination: float = 0.1) -> None:
        """Train anomaly detection model"""
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100,
        )
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_trained = True
        logger.info(f"Anomaly detector trained on {X.shape[0]} samples")

    def predict(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Predict anomalies and return scores (-1: anomaly, 1: normal)"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        scores = -self.model.score_samples(X_scaled)
        scores = np.clip((scores - scores.min()) / (scores.max() - scores.min() + 1e-8), 0, 1)

        return predictions, scores

    def predict_single(self, features: list) -> tuple[bool, float]:
        """Predict single invoice anomaly"""
        X = np.array([features]).reshape(1, -1)
        predictions, scores = self.predict(X)
        is_anomaly = predictions[0] == -1
        confidence = scores[0]
        return is_anomaly, confidence

    def save(self) -> None:
        """Save model to disk"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": self.model, "scaler": self.scaler}, self.model_path)
        logger.info(f"Model saved to {self.model_path}")

    def load(self) -> None:
        """Load model from disk"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        data = joblib.load(self.model_path)
        self.model = data["model"]
        self.scaler = data["scaler"]
        self.is_trained = True
        logger.info(f"Model loaded from {self.model_path}")


# Global instance
anomaly_detector = AnomalyDetector()
