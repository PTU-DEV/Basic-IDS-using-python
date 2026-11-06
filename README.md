
# 🛡️ AI-Powered Intrusion Detection System (IDS)
A Machine Learning + Packet Sniffing based real-time Intrusion Detection System built using **Python**, **Scapy**, **RandomForest**, and a **Streamlit Dashboard**.

This project captures live network packets, extracts features, classifies traffic as *normal* or *intrusive*, logs intrusions, and visualizes them on a real-time dashboard.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Why This Project?](#why-this-project)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Demo Workflow](#demo-workflow)
- [Future Enhancements](#future-enhancements)

---

## 🔍 Overview
Intrusion Detection Systems (IDS) are essential in cybersecurity for monitoring network traffic and detecting malicious activities.  
This project implements a **host-based IDS** that detects anomalies using:

- Live Packet Capture (Scapy)
- Machine Learning Classification (RandomForest)
- Real-time Data Visualization (Streamlit)
- Logging & Analysis (CSV Log Storage)

The system is lightweight and suitable for academic, training, and small-scale enterprise environments.

---

## ❓ Why This Project?
Most IDS solutions are large, complex, and not beginner-friendly.  
This project aims to:

- Simplify how IDS works internally  
- Demonstrate real packet sniffing  
- Connect ML with live network features  
- Provide an interactive analytics dashboard  

This project is also *fully reproducible* for training, internships, and demonstrations.

---

## ⭐ Features

### 🔹 **1. Real-time Packet Sniffing**
Uses Scapy to capture network packets (IP/TCP/UDP).

### 🔹 **2. ML-Powered Intrusion Classification**
Classifies traffic using a RandomForest model trained on a subset of NSL-KDD dataset features.

### 🔹 **3. Intrusion Logging**
Every suspicious event is logged into:
```

logs/ids_alerts.csv

```

Stored fields:
- Timestamp  
- Source IP  
- Destination IP  
- Packet Length  
- TTL  
- Flags  
- Prediction result  

### 🔹 **4. Real-time Streamlit Dashboard**
Visualizations include:
- Number of intrusions  
- Top attacker IPs  
- Intrusion timeline chart  
- Latest events table  
- Traffic statistics  

### 🔹 **5. Modular Codebase**
Separated into:
- Training
- Sniffing
- Logging
- Dashboard

---

## 🏗️ Architecture

```

```
           ┌──────────────────────────┐
           │      Packet Sniffer      │
           │       (Scapy)            │
           └─────────────┬────────────┘
                         │ Extract 3 features
                         ▼
           ┌──────────────────────────┐
           │   ML Classifier (RF)     │
           │  normal / intrusion      │
           └─────────────┬────────────┘
                         ▼
           ┌──────────────────────────┐
           │   Intrusion Logger       │
           │ writes logs → CSV        │
           └─────────────┬────────────┘
                         ▼
           ┌──────────────────────────┐
           │   Streamlit Dashboard    │
           │  reads & visualizes logs │
           └──────────────────────────┘
```

```

---

## 🧰 Tech Stack

| Component        | Technology |
|------------------|------------|
| Packet Capture   | Scapy |
| ML Model         | RandomForestClassifier |
| Dashboard        | Streamlit |
| Data Processing  | Pandas |
| Environment Mgmt | uv (Python package manager) |
| Dataset          | NSL-KDD |

---

## 📦 Dataset
Dataset used: **NSL-KDD (KDDTest.csv)**  
Source: Kaggle  
Converted from `.arff` → `.csv` for easier ML processing.

We extracted 3 lightweight numerical features for real-time matching:

| Feature | Meaning |
|---------|---------|
| src_bytes | proxy for packet length |
| dst_bytes | proxy for TTL |
| wrong_fragment | proxy for TCP flags |

These match the 3 features the live sniffer extracts.

---

## 📁 Project Structure
```

IDS/
│
├── dataset/
│     └── KDDTest.csv
│
├── models/
│     └── sniffer_model.joblib
│
├── logs/
│     └── ids_alerts.csv
│
├── src/
│     ├── load_dataset.py
│     ├── train_sniffer_model.py
│     ├── live_sniffer.py
│     └── dashboard.py
│
└── README.md

```

---

## ⚙️ How It Works

### **Step 1 — Train ML Model**
- Dataset is converted to CSV.
- Only 3 numerical features are selected.
- RandomForestClassifier is trained.
- Model saved into `models/sniffer_model.joblib`.

### **Step 2 — Live Packet Sniffing**
- Scapy captures IP/TCP/UDP packets.
- Extracts 3 real-time features:
  - packet_length  
  - ttl  
  - tcp_flags  

### **Step 3 — ML Prediction**
The model predicts:
- `0` → Normal  
- `1` → Intrusion  

### **Step 4 — Logging**
If prediction is 1 (intrusion), IDS logs event into:
```

logs/ids_alerts.csv

````

### **Step 5 — Real-time Dashboard**
Dashboard reads the CSV log every few seconds and updates:
- Intrusion timeline graph  
- Recent alerts  
- Top attacker IPs  
- Traffic statistics  

---

## 🚀 Installation

### 1️⃣ Install dependencies via **uv**
```sh
uv add scapy pandas scikit-learn joblib streamlit matplotlib
````

### 2️⃣ Run dataset converter (optional)

```sh
uv run src/load_dataset.py
```

---

## ▶️ How to Run

### 1️⃣ Train the ML model

```sh
uv run src/train_sniffer_model.py
```

### 2️⃣ Start the Live IDS Sniffer

```sh
uv run src/live_sniffer.py
```

### 3️⃣ Start the Dashboard (in another terminal)

```sh
uv run streamlit run src/dashboard.py
```

---

## 🧪 Demo Workflow

1. Start `live_sniffer.py`
2. Start `dashboard.py`
3. Generate traffic:

   ```sh
   ping google.com
   ```
4. Watch dashboard update in real-time
5. Check logs at `logs/ids_alerts.csv`

---

## 🚀 Future Enhancements

### 🔹 Enhance ML Model

* Use deep learning (LSTM, CNN)
* Add more packet-level features
* Retrain using real captured traffic

### 🔹 Add Security Features

* Automatic IP blocking (Windows/Linux firewall)
* Email or SMS alert integration
* Push alerts to mobile devices

### 🔹 Visualization Upgrades

* GeoIP Mapping (attacker locations)
* Advanced heatmaps
* Exportable PDF reports

---

## 📘 Conclusion

This project demonstrates how to integrate machine learning with real-time network monitoring to create a practical intrusion detection system.
It is fully modular, extendable, and ideal for cybersecurity internships, training labs, and academic submissions.

---

## 🙌 Author
[Roushan](https://github.com/Roushan-kr)

Reuse for teaching basic cyber concept to student.

```
