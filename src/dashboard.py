import streamlit as st
import pandas as pd
from pathlib import Path
import time

st.set_page_config(page_title="IDS Dashboard", layout="wide")

project_root = Path(__file__).resolve().parents[1]
log_file = project_root / "logs" / "ids_alerts.csv"

st.title("🛡️ Intrusion Detection System Dashboard")
st.caption("Real-time monitoring of network intrusions & traffic behavior")

# --- Auto-refresh setup ---
refresh_rate = st.sidebar.slider("Refresh every (seconds)", 1, 10, 3)
st.sidebar.info("IDS must be running in another terminal.\nThis dashboard pulls logs live.")

# --- Main loop function ---
def load_data():
    if log_file.exists():
        return pd.read_csv(log_file)
    else:
        return pd.DataFrame(columns=["timestamp", "src_ip", "dst_ip", "pkt_len", "ttl", "flags", "prediction"])

# --- Real-time UI update ---
placeholder = st.empty()

while True:
    df = load_data()

    with placeholder.container():

        if df.empty:
            st.warning("No intrusion logs yet. Waiting for data...")
        else:
            st.success(f"Total Intrusions Logged: {df.shape[0]}")

            # --- Section 1: Intrusion table ---
            st.subheader("Latest Intrusions")
            st.dataframe(df.tail(15), use_container_width=True)

            # --- Section 2: Top attacker IPs ---
            st.subheader("Top Attacker IPs")
            top_attackers = df["src_ip"].value_counts().head(10)
            st.bar_chart(top_attackers)

            # --- Section 3: Intrusion timeline ---
            st.subheader("Intrusions Over Time")
            timeline = df.groupby("timestamp").size()
            st.line_chart(timeline)

            # --- Section 4: Traffic statistics ---
            st.subheader("Traffic Feature Statistics")
            st.write(df[["pkt_len", "ttl", "flags"]].describe())

    time.sleep(refresh_rate)
