import boto3
import os
from botocore import UNSIGNED
from botocore.client import Config
from datetime import datetime, timedelta

# ================= CONFIGURATION =================
# AWS Bucket for Himawari-9 (Public)
BUCKET_NAME = 'noaa-himawari9'
LOCAL_DOWNLOAD_DIR = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/satellite files'

# Date Range: March 1, 2025 to May 31, 2025
START_DATE = datetime(2025, 3, 1)
END_DATE = datetime(2025, 3, 31)

# Bands for Brightness Temperature (IR)
# Band 14 (11.2 µm) and Band 15 (12.4 µm)
TARGET_BANDS = [14, 15]

# Himawari Full Disk is split into 10 segments (1-10)
# You generally need all 10 to reconstruct the full disk image.
TARGET_SEGMENTS = range(1, 11) 

# =================================================

def download_himawari_aws():
    # 1. Setup AWS S3 Client for anonymous access
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    if not os.path.exists(LOCAL_DOWNLOAD_DIR):
        os.makedirs(LOCAL_DOWNLOAD_DIR)

    print(f"Starting download from s3://{BUCKET_NAME}...")
    print(f"Period: {START_DATE} to {END_DATE}")
    print(f"Bands: {TARGET_BANDS}")

    current_time = START_DATE
    while current_time <= END_DATE:
        # Time components for path construction
        year = current_time.strftime("%Y")
        month = current_time.strftime("%m")
        day = current_time.strftime("%d")
        hhmm = current_time.strftime("%H%M")
        
        # AWS S3 Path Structure: AHI-L1b-FLDK/YYYY/MM/DD/HHMM/
        prefix = f"AHI-L1b-FLDK/{year}/{month}/{day}/{hhmm}/"

        for band in TARGET_BANDS:
            for seg in TARGET_SEGMENTS:
                # Construct the standard filename
                # Format: HS_H09_YYYYMMDD_hhmm_Bxx_FLDK_R20_Szz10.DAT.bz2
                # R20 = 2km resolution (Standard for IR bands 14/15)
                # Szz10 = Segment zz of 10
                
                band_str = f"B{band:02}"
                seg_str = f"S{seg:02}10" 
                file_date_str = current_time.strftime("%Y%m%d_%H%M")
                
                filename = f"HS_H09_{file_date_str}_{band_str}_FLDK_R20_{seg_str}.DAT.bz2"
                key = prefix + filename
                local_path = os.path.join(LOCAL_DOWNLOAD_DIR, filename)

                # Skip if already exists
                if os.path.exists(local_path):
                    # print(f"Skipping {filename} (exists)")
                    continue

                try:
                    print(f"Downloading: {key}")
                    s3.download_file(BUCKET_NAME, key, local_path)
                except Exception as e:
                    # If 404, file might not exist (maintenance, eclipse, etc.)
                    print(f"Failed to download {key}: {e}")

        # Advance 10 minutes (standard Himawari observation cycle)
        current_time += timedelta(minutes=10)

    print("Download complete.")

if __name__ == "__main__":
    download_himawari_aws()