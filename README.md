# Carbon-Aware Predictive Load Shifting

This is a personal open-data portfolio project exploring carbon-aware load shifting.

The current version is **Level 0: Offline Backtest**.

This project does not use employer data, internal systems, or real building-control actions.

---

## Level 0: Offline Backtest

This first version uses sample data to test a basic idea:

Can a portion of electricity load be shifted away from high-carbon hours and moved into lower-carbon hours?

The app compares a baseline load schedule against a simple optimized schedule and estimates the change in emissions.

---

## What This Version Does

- Creates sample building-load data
- Creates sample carbon-intensity data
- Identifies high-carbon and low-carbon hours
- Shifts a configurable fraction of load
- Compares baseline vs optimized emissions
- Displays results in a Streamlit dashboard

---

## How to Run in GitHub Codespaces

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate sample data:

```bash
python scripts/make_sample_data.py
```

Run the Streamlit app:

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Open port 8501 from the Codespaces Ports tab.

---

## Project Status

Level 0 is in progress.