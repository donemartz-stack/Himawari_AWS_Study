import os
import bz2
import glob
import shutil
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from satpy import Scene

# ================= CONFIGURATION =================
# 1. PATHS
# Directory where your .DAT.BZ2 files are located
DATA_DIR = '/Users/danwilliammartinez/Desktop/Himawari_AWS_Study/himawari_data_flat'
# Directory to store temporary unzipped files (created/deleted automatically)
TEMP_DIR = os.path.join(DATA_DIR, "temp_processing")
# Output CSV filename
OUTPUT_CSV = 'himawari_ph_temperature.csv'

# 2. LOCATION (Orani, Bataan)
TARGET_LAT = 14.77083
TARGET_LON = 120.45537

# 3. SETTINGS
# Bands to extract (IR Bands 14 & 15)
BANDS = ['B14', 'B15']
# Set to True for Celsius, False for Kelvin
SAVE_IN_CELSIUS = False 
# =================================================

def decompress_group(bz2_files, output_dir):
    """
    Decompresses a list of .bz2 files to a specific directory.
    Returns the list of new file paths.
    """
    decompressed_paths = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for bz2_file in bz2_files:
        # Remove .bz2 extension for the output filename
        basename = os.path.basename(bz2_file).replace('.bz2', '')
        out_path = os.path.join(output_dir, basename)
        
        # Decompress only if it doesn't exist yet
        if not os.path.exists(out_path):
            with bz2.BZ2File(bz2_file, 'rb') as f_in:
                with open(out_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        decompressed_paths.append(out_path)
    return decompressed_paths

def process_himawari_data():
    # 1. Find all compressed files
    all_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.DAT.bz2")))
    if not all_files:
        print(f"No .DAT.bz2 files found in {DATA_DIR}")
        return

    # 2. Group files by Timestamp (YYYYMMDD_hhmm)
    # This ensures we process all segments for one specific time together.
    grouped_files = {}
    for f in all_files:
        # Extract date/time from standard filename:
        # HS_H09_YYYYMMDD_hhmm_Bxx_...
        parts = os.path.basename(f).split('_')
        if len(parts) > 3:
            # parts[2] = YYYYMMDD, parts[3] = hhmm
            ts_key = f"{parts[2]}_{parts[3]}"
            if ts_key not in grouped_files:
                grouped_files[ts_key] = []
            grouped_files[ts_key].append(f)

    results = []
    print(f"Found {len(grouped_files)} unique observation times.")

    # 3. Process each timestamp group
    for ts_key, file_list in grouped_files.items():
        try:
            # --- A. TIMEZONE CONVERSION ---
            # Parse UTC time from filename string
            utc_time = datetime.strptime(ts_key, "%Y%m%d_%H%M")
            # Add 8 hours for Philippine Standard Time (PST)
            ph_time = utc_time + timedelta(hours=8)
            
            print(f"Processing: {ph_time.strftime('%Y-%m-%d %H:%M:%S')} (PST)...", end=" ")

            # --- B. DECOMPRESSION ---
            # Unzip files to temp folder
            current_files = decompress_group(file_list, TEMP_DIR)

            # --- C. LOAD DATA ---
            # Load the scene with Satpy
            # 'ahi_hsd' reader handles binary format & calibration automatically
            scn = Scene(filenames=current_files, reader='ahi_hsd')
            scn.load(BANDS)

            # --- D. GEOLOCATION (UPDATED) ---
            # Get the AreaDefinition (geometry) from the first band
            area = scn[BANDS[0]].attrs['area']
            
            # Use the new method to avoid DeprecationWarning
            # This returns the nearest integer indices (row, col)
            row_idx, col_idx = area.get_array_indices_from_lonlat(TARGET_LON, TARGET_LAT)
            
            # Ensure indices are standard Python integers
            row_idx = int(row_idx)
            col_idx = int(col_idx)

            # Prepare row data
            row_data = {
                'timestamp_ph': ph_time,
                'timestamp_utc': utc_time,
                'latitude': TARGET_LAT,
                'longitude': TARGET_LON
            }

            # --- E. EXTRACT VALUES ---
            valid_extraction = True
            for band in BANDS:
                # Check if the calculated pixel is actually inside the image array
                # (This protects against segments that don't cover the location)
                if (0 <= row_idx < scn[band].shape[0]) and (0 <= col_idx < scn[band].shape[1]):
                    
                    # Extract value (Kelvin)
                    val = scn[band][row_idx, col_idx].values.item()
                    
                    # Optional: Convert to Celsius
                    if SAVE_IN_CELSIUS:
                        val = val - 273.15
                        
                    row_data[band] = val
                else:
                    # Coordinate is outside the loaded segment(s)
                    valid_extraction = False
                    row_data[band] = np.nan
            
            if valid_extraction:
                results.append(row_data)
                print("Done.")
            else:
                print("Out of bounds (Location not in loaded segments).")

            # Clean memory for this loop
            del scn

        except Exception as e:
            print(f"\nError processing {ts_key}: {e}")
        
        finally:
            # --- F. CLEANUP ---
            # Delete the temp folder contents to save disk space
            if os.path.exists(TEMP_DIR):
                shutil.rmtree(TEMP_DIR)

    # 4. Save results to CSV
    if results:
        df = pd.DataFrame(results)
        
        # Reorder columns for readability
        cols = ['timestamp_ph', 'timestamp_utc', 'latitude', 'longitude'] + BANDS
        df = df[cols]
        
        df.to_csv(OUTPUT_CSV, index=False)
        print("-" * 30)
        print(f"Processing complete.")
        print(f"Data saved to: {os.path.abspath(OUTPUT_CSV)}")
        print("-" * 30)
        print(df.head())
    else:
        print("No valid data was extracted. Please check if your downloaded segments cover the Philippines (Lat ~14N).")

if __name__ == "__main__":
    process_himawari_data()