from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

project_root = Path(__file__).resolve().parents[1]
dataset_file = project_root / "dataset" / "KDDTest.csv"

print("Loading dataset:", dataset_file)
df = pd.read_csv(dataset_file)

print("Initial shape:", df.shape)

# Rename target column if needed
if 'class' not in df.columns:
    df.rename(columns={df.columns[-1]: 'class'}, inplace=True)

y = df['class']
X = df.drop(columns=['class'])

# Encode attacks: normal = 0, anomaly = 1
y = y.apply(lambda x: 0 if str(x).lower() == "normal" else 1)

# Encode categorical features into numbers
label_encoders = {}
for col in X.columns:
    if X[col].dtype == object:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

print("After encoding shape:", X.shape)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=150)
model.fit(X_train, y_train)

# Save model artifact
model_path = project_root / "models" / "ids_model.joblib"
dump(model, model_path)

print(f"🎯 Model trained successfully and saved at: {model_path}")
print(f"✔ Accuracy (Train): {model.score(X_train, y_train):.4f}")
print(f"✔ Accuracy (Test): {model.score(X_test, y_test):.4f}")
