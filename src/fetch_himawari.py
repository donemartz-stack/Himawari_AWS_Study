"""
fetch_himawari.py
Purpose: Download Himawari satellite Band 14 and Band 15 data
and save locally for analysis.

Workflow:
- Specify coordinates, date, and bands
- Download data to local 'data/' folder
- Compatible with your Git workflow (.gitignore prevents pushing large files)
"""

import os
from datetime import datetime
import requests  # or your preferred API client

# =========================
# Configuration
# =========================
DATA_DIR = "../data/raw"  # relative path from src/
BANDS = [14, 15]
COORDINATES = (14.77083, 120.45537)  # latitude, longitude
START_DATE = "2025-03-01"
END_DATE = "2025-06-30"

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# Function to fetch a single band
# =========================
def fetch_band_data(band, date, coords):
    """
    Placeholder function to fetch Himawari band data.
    Replace with actual API call or download logic.
    """
    lat, lon = coords
    filename = f"band{band}_{date.replace('-', '')}.nc"
    filepath = os.path.join(DATA_DIR, filename)
    
    # Example: simulate download (replace with actual request)
    print(f"Fetching Band {band} for {date} at {lat},{lon} ...")
    # requests.get("API_ENDPOINT", params=...) → save to filepath
    # For now, just create empty placeholder file
    with open(filepath, "w") as f:
        f.write(f"Placeholder for Band {band}, {date}, {lat},{lon}\n")
    
    print(f"Saved to {filepath}")
    return filepath

# =========================
# Main script
# =========================
if __name__ == "__main__":
    # Generate date range (simple example, daily)
    from datetime import timedelta, date

    def daterange(start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        for n in range((end - start).days + 1):
            yield start + timedelta(n)

    # Loop over dates and bands
    for single_date in daterange(START_DATE, END_DATE):
        date_str = single_date.strftime("%Y-%m-%d")
        for band in BANDS:
            fetch_band_data(band, date_str, COORDINATES)

    print("All downloads complete.")
