import os
import torch
import librosa
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import joblib

from transformers import Wav2Vec2Processor, Wav2Vec2Model

# Set device (CPU only, since AMD Radeon isn't CUDA-compatible)
device = torch.device("cpu")

# Load pre-trained model and processor from Hugging Face
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base").to(device)

# Supported emotions (can be adjusted)
TARGET_EMOTIONS = ['fear', 'neutral']

# Dataset root path
DATASETS_PATH = "datasets"

# Map dataset labels (adjust if needed)
def get_label_from_filename(filename, dataset_name):
    if dataset_name == "TESS":
        for emotion in TARGET_EMOTIONS:
            if emotion in filename.lower():
                return emotion
    elif dataset_name == "CREMA-D":
        parts = filename.split('_')
        code = parts[-2]
        label_map = {
            'SAD': 'neutral', 'ANG': 'neutral', 'DIS': 'neutral', 'FEA': 'fear',
            'HAP': 'neutral', 'NEU': 'neutral'
        }
        return label_map.get(code, 'neutral')
    elif dataset_name == "RAVDESS":
        parts = filename.split('-')
        emo_code = int(parts[2])
        label_map = {
            1: 'neutral', 2: 'neutral', 3: 'neutral', 4: 'neutral',
            5: 'neutral', 6: 'fear', 7: 'neutral', 8: 'neutral'
        }
        return label_map.get(emo_code, 'neutral')
    elif dataset_name == "SAVEE":
        if 'f' in filename.lower():
            return 'fear'
        return 'neutral'
    return None

# Extract features using Wav2Vec2
def extract_features(file_path):
    try:
        waveform, sr = librosa.load(file_path, sr=16000)
        input_values = processor(waveform, return_tensors="pt", sampling_rate=16000).input_values.to(device)
        with torch.no_grad():
            embeddings = model(input_values).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        return embeddings
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Aggregate all features and labels
features = []
labels = []

# Process datasets
for dataset in os.listdir(DATASETS_PATH):
    dataset_path = os.path.join(DATASETS_PATH, dataset)
    print(f"\nProcessing dataset: {dataset}")

    for root, _, files in os.walk(dataset_path):
        for file in tqdm(files, desc=f"Processing files in {dataset}"):
            if not file.endswith('.wav'):
                continue

            label = get_label_from_filename(file, dataset)
            if label not in TARGET_EMOTIONS:
                continue

            file_path = os.path.join(root, file)
            print(f"→ {file} ({label})")

            feat = extract_features(file_path)
            if feat is not None:
                features.append(feat)
                labels.append(label)

# Encode labels
le = LabelEncoder()
encoded_labels = le.fit_transform(labels)

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(features, encoded_labels, test_size=0.2, random_state=42)

# Train classifier
clf = make_pipeline(StandardScaler(), SVC(kernel="linear", probability=True))
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))
print(f"✅ Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump({"model": clf, "label_encoder": le}, "models/fear_model_wav2vec.pkl")
print("✅ Model saved as 'models/fear_model_wav2vec.pkl'")
