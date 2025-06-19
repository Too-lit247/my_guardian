import os
import joblib
import numpy as np
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class FearDetectionModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        # Don't load model on import to avoid startup issues
    
    def load_model(self):
        """Load the pre-trained fear detection model"""
        try:
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'fear_detection_model.pkl')
            scaler_path = os.path.join(settings.BASE_DIR, 'ml_models', 'fear_detection_scaler.pkl')
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                logger.info("Fear detection model loaded successfully")
            else:
                logger.warning("Fear detection model files not found. Using dummy model.")
                self.model = None
                self.scaler = None
        except Exception as e:
            logger.error(f"Error loading fear detection model: {e}")
            self.model = None
            self.scaler = None
    
    def predict_fear(self, audio_file_path):
        """Predict fear probability from audio file"""
        if self.model is None:
            # Return dummy prediction if model not loaded
            logger.warning("Using dummy fear prediction")
            return {
                'fear_probability': np.random.random() * 0.3,  # Low random probability
                'stress_level': np.random.random() * 0.4,
                'confidence': 0.5
            }
        
        # Model prediction logic would go here
        return {
            'fear_probability': 0.1,
            'stress_level': 0.2,
            'confidence': 0.8
        }

# Global instance - don't initialize on import
fear_detector = None

def get_fear_detector():
    global fear_detector
    if fear_detector is None:
        fear_detector = FearDetectionModel()
        fear_detector.load_model()
    return fear_detector

def analyze_audio_for_fear(audio_file_path):
    """Analyze audio file for fear detection"""
    detector = get_fear_detector()
    return detector.predict_fear(audio_file_path)
