import os
import subprocess
from datetime import datetime, timedelta

# ==============================
# USER SETTINGS
# ==============================
START_DATE = datetime(2025, 4, 15)
END_DATE   = datetime(2025, 5, 31)

BANDS = ["B13", "B14"]
SATELLITE = "noaa-himawari9"
PRODUCT = "AHI-L1b-FLDK"

DOWNLOAD_DIR = "himawari_B13_B14_202503_202505"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ==============================
# DOWNLOAD FUNCTION
# ==============================
def download_file(s3_path, local_path):
    cmd = [
        "aws", "s3", "cp",
        s3_path,
        local_path,
        "--no-sign-request"
    ]
    subprocess.run(cmd)

# ==============================
# LOOP THROUGH DATES
# ==============================
current = START_DATE

while current <= END_DATE:
    date_str = current.strftime("%Y/%m/%d")
    date_compact = current.strftime("%Y%m%d")

    for hour in range(24):
        for minute in range(0, 60, 10):

            time_str = f"{hour:02d}{minute:02d}"

            for BAND in BANDS:

                filename = f"HS_H09_{date_compact}_{time_str}_{BAND}_FLDK_R20_S0110.DAT.bz2"
                s3_path = f"s3://{SATELLITE}/{PRODUCT}/{date_str}/{time_str}/{filename}"
                local_path = os.path.join(DOWNLOAD_DIR, filename)

                print("Downloading:", filename)
                download_file(s3_path, local_path)

    current += timedelta(days=1)

print("Download completed.")