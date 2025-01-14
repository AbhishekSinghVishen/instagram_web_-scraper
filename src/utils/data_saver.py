# src/utils/data_saver.py
import os
import json

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

def save_raw_data(username, html):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    with open(f"{RAW_DATA_DIR}/{username}.html", "w", encoding="utf-8") as file:
        file.write(html)

def save_processed_data(username, data):
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    with open(f"{PROCESSED_DATA_DIR}/{username}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
