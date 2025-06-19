from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
import librosa
import numpy as np
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2Model
import joblib
import os

# Initialize FastAPI app
app = FastAPI()

# Load pre-trained Wav2Vec2 model and processor
device = torch.device("cpu")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base").to(device)

# Load trained classifier and label encoder
MODEL_PATH = "models/fear_model_wav2vec.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Trained model not found at {MODEL_PATH}")
model_data = joblib.load(MODEL_PATH)
clf = model_data["model"]
label_encoder = model_data["label_encoder"]

# Function to extract features from audio file
def extract_features(file_path: str):
    try:
        waveform, sr = librosa.load(file_path, sr=16000)
        input_values = processor(waveform, return_tensors="pt", sampling_rate=16000).input_values.to(device)
        with torch.no_grad():
            embeddings = model(input_values).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        return embeddings
    except Exception as e:
        raise ValueError(f"Error processing audio file: {e}")

# Endpoint to predict emotion from uploaded audio file
@app.post("/predict/")
async def predict_emotion(file: UploadFile = File(...)):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported")

    try:
        # Save uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Extract features
        features = extract_features(temp_file_path)

        # Predict emotion
        prediction = clf.predict([features])
        predicted_label = label_encoder.inverse_transform(prediction)[0]

        # Clean up temporary file
        os.remove(temp_file_path)

        return {"filename": file.filename, "predicted_emotion": predicted_label}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)