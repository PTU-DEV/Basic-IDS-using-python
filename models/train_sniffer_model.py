from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# Resolve project root (IDS/)
project_root = Path(__file__).resolve().parents[1]
dataset_file = project_root / "dataset" / "KDDTest.csv"

print("Loading dataset:", dataset_file)
df = pd.read_csv(dataset_file)

print("Shape:", df.shape)

# Make sure target column exists and is called 'class'
if "class" not in df.columns:
    df.rename(columns={df.columns[-1]: "class"}, inplace=True)

# Binary labels: 0 = normal, 1 = anomaly/attack
df["class"] = df["class"].apply(
    lambda x: 0 if str(x).strip().lower() == "normal" else 1
)

# ---- Use 3 numeric columns from NSL-KDD as proxy features ----
# (They exist in your ARFF snippet)
feature_cols = ["src_bytes", "dst_bytes", "wrong_fragment"]

for col in feature_cols:
    if col not in df.columns:
        raise ValueError(f"Expected column '{col}' not found in dataset!")

X = df[feature_cols].copy()
y = df["class"]

# Encode any non-numeric columns if needed (should already be numeric here)
for col in X.columns:
    if X[col].dtype == object:   # << fixed: dtype, not dtypes
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])

print("Using features:", list(X.columns))
print("X dtype summary:")
print(X.dtypes)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model on these 3 features
model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

model_out = project_root / "models" / "sniffer_model.joblib"
dump(model, model_out)

print("🎯 Model trained successfully:", model_out)
print("Train Accuracy:", model.score(X_train, y_train))
print("Test Accuracy:", model.score(X_test, y_test))
