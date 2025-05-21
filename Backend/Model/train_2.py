import os
import torch
import librosa
from torch import nn
from torch.utils.data import DataLoader, Dataset
from transformers import Wav2Vec2Processor, Wav2Vec2Model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

device = torch.device("cpu")

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
base_model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")

# Freeze lower layers
for param in base_model.parameters():
    param.requires_grad = False

# Unfreeze last transformer layers
for layer in base_model.encoder.layers[-6:]:  # Unfreeze last 6 layers
    for param in layer.parameters():
        param.requires_grad = True

class FearDataset(Dataset):
    def __init__(self, file_paths, labels):
        self.file_paths = file_paths
        self.labels = labels

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        path = self.file_paths[idx]
        waveform, _ = librosa.load(path, sr=16000)
        inputs = processor(waveform, return_tensors="pt", sampling_rate=16000, padding=True, truncation=True, max_length=16000*5)
        inputs = {k: v.squeeze(0) for k, v in inputs.items()}
        label = torch.tensor(self.labels[idx], dtype=torch.long)
        return inputs, label

class FearClassifier(nn.Module):
    def __init__(self, base_model, num_classes):
        super(FearClassifier, self).__init__()
        self.base = base_model
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.base.config.hidden_size, num_classes)

    def forward(self, input_values, attention_mask=None):
        outputs = self.base(input_values, attention_mask=attention_mask)
        hidden_state = outputs.last_hidden_state
        pooled = hidden_state.mean(dim=1)
        x = self.dropout(pooled)
        x = self.classifier(x)
        return x

DATASETS_PATH = "datasets"
TARGET_EMOTIONS = ['fear', 'neutral']

def get_label_from_filename(filename, dataset_name):
    if dataset_name == "TESS":
        for emotion in TARGET_EMOTIONS:
            if emotion in filename.lower():
                return emotion
    elif dataset_name == "CREMA-D":
        parts = filename.split('_')
        code = parts[-2]
        label_map = {'SAD': 'neutral', 'ANG': 'neutral', 'DIS': 'neutral', 'FEA': 'fear', 'HAP': 'neutral', 'NEU': 'neutral'}
        return label_map.get(code, 'neutral')
    elif dataset_name == "RAVDESS":
        parts = filename.split('-')
        emo_code = int(parts[2])
        label_map = {1: 'neutral', 2: 'neutral', 3: 'neutral', 4: 'neutral', 5: 'neutral', 6: 'fear', 7: 'neutral', 8: 'neutral'}
        return label_map.get(emo_code, 'neutral')
    elif dataset_name == "SAVEE":
        if 'f' in filename.lower():
            return 'fear'
        return 'neutral'
    return None

file_paths = []
labels = []

for dataset in os.listdir(DATASETS_PATH):
    dataset_path = os.path.join(DATASETS_PATH, dataset)
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.wav'):
                label = get_label_from_filename(file, dataset)
                if label in TARGET_EMOTIONS:
                    file_paths.append(os.path.join(root, file))
                    labels.append(label)

le = LabelEncoder()
encoded_labels = le.fit_transform(labels)

train_files, val_files, train_labels, val_labels = train_test_split(file_paths, encoded_labels, test_size=0.2, random_state=42)

train_dataset = FearDataset(train_files, train_labels)
val_dataset = FearDataset(val_files, val_labels)

train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=2)

model = FearClassifier(base_model, num_classes=len(le.classes_)).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW([
    {"params": model.base.encoder.layers[-6:].parameters(), "lr": 1e-5},  # Fine-tuning Wav2Vec2 (slow learning rate)
    {"params": model.classifier.parameters(), "lr": 1e-4}  # Faster learning for classifier
])

num_epochs = 8
accumulation_steps = 4  # accumulate gradients to simulate bigger batch

for epoch in range(num_epochs):
    model.train()
    running_loss = 0
    optimizer.zero_grad()

    for i, (batch_inputs, batch_labels) in enumerate(train_loader):
        input_values = batch_inputs["input_values"].to(device)
        attention_mask = batch_inputs.get("attention_mask", None)
        if attention_mask is not None:
            attention_mask = attention_mask.to(device)

        batch_labels = batch_labels.to(device)

        outputs = model(input_values, attention_mask)
        loss = criterion(outputs, batch_labels)
        loss = loss / accumulation_steps
        loss.backward()

        if (i + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()

        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss:.4f}")

torch.save({
    'model_state_dict': model.state_dict(),
    'label_encoder': le
}, "models/fear_classifier_finetuned.pth")
print("✅ Model saved as 'models/fear_classifier_finetuned.pth'")
