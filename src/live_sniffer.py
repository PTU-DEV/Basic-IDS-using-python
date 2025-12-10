from scapy.all import sniff, IP, TCP, UDP
from joblib import load
from pathlib import Path
import numpy as np
import csv
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# Resolve project root
project_root = Path(__file__).resolve().parents[1]
model_path = project_root / "models" / "sniffer_model.joblib"
log_file = project_root / "logs" / "ids_alerts.csv"

print("Loading model:", model_path)
model = load(model_path)

# Ensure log file exists
if not log_file.exists():
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "src_ip", "dst_ip", "pkt_len", "ttl", "flags", "prediction"])


def extract_features(packet):
    pkt_len = len(packet)
    ttl = packet[IP].ttl if packet.haslayer(IP) else 0

    if packet.haslayer(TCP):
        flags = int(packet[TCP].flags)
    else:
        flags = 0

    # SAME 3 FEATURES AS TRAINING
    return np.array([pkt_len, ttl, flags]).reshape(1, -1)


def log_intrusion(src, dst, pkt_len, ttl, flags, pred):
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), src, dst, pkt_len, ttl, flags, pred])


def analyze(packet):
    if packet.haslayer(IP):
        features = extract_features(packet)
        prediction = model.predict(features)[0]

        src = packet[IP].src
        dst = packet[IP].dst

        pkt_len = features[0][0]
        ttl = features[0][1]
        flags = features[0][2]

        if prediction == 1:
            print(f"⚠️ Intrusion Detected! {src} → {dst}")
            log_intrusion(src, dst, pkt_len, ttl, flags, prediction)
        else:
            print(f"✔ Normal Traffic: {src} → {dst}")


print("🔍 Live IDS running… Logging enabled. Press CTRL+C to stop.")

sniff(prn=analyze, store=False)
