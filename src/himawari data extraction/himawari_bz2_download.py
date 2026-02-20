import boto3
import botocore
from botocore.config import Config
import os
from datetime import datetime, timedelta

def download_himawari_data_flat(start_date, end_date, output_dir='himawari_data_flat'):
    """
    Downloads Himawari-9 Band 14 and 15 HSD data from AWS S3 into a single folder.
    """
    # 1. Configure anonymous access to the public bucket
    s3 = boto3.client('s3', config=Config(signature_version=botocore.UNSIGNED))
    bucket_name = 'noaa-himawari9'
    
    # Create the single output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    # 2. Define parameters
    bands = ['B14', 'B15']
    segments = range(1, 11) # Segments 01 through 10
    
    # 3. Iterate through the date range
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        year = current_date.strftime('%Y')
        month = current_date.strftime('%m')
        day = current_date.strftime('%d')
        
        print(f"Processing date: {date_str}")

        # Iterate through 24 hours in 10-minute intervals
        for hour in range(24):
            for minute in range(0, 60, 10):
                time_str = f"{hour:02d}{minute:02d}"
                
                # AWS S3 Path (Prefix) - Required to find the file in the bucket
                prefix = f"AHI-L1b-FLDK/{year}/{month}/{day}/{time_str}/"
                
                for band in bands:
                    for seg in segments:
                        # Construct the Filename
                        file_name = (
                            f"HS_H09_{date_str}_{time_str}_{band}_FLDK_R20_S{seg:02d}10.DAT.bz2"
                        )
                        
                        # The full key to the object in S3
                        object_key = prefix + file_name
                        
                        # Local file path - SAVING TO ROOT FOLDER ONLY
                        local_file_path = os.path.join(output_dir, file_name)
                        
                        # Check if file exists locally before downloading
                        if os.path.exists(local_file_path):
                            # Optional: Print less frequently to reduce console noise
                            continue

                        try:
                            s3.download_file(bucket_name, object_key, local_file_path)
                            # Print success (optional: comment out to speed up console)
                            print(f"Downloaded: {file_name}")
                        except botocore.exceptions.ClientError as e:
                            if e.response['Error']['Code'] == "404":
                                # File missing on S3 (common for specific timelines)
                                pass 
                            else:
                                print(f"Error downloading {file_name}: {e}")

        current_date += timedelta(days=1)

if __name__ == "__main__":
    # Define period: March 1, 2025 to May 31, 2025
    start_dt = datetime(2025, 4, 16, 00, 00)
    end_dt = datetime(2025, 4, 30, 23, 50)
    
    # WARNING: Saving ~260,000 files into a single folder may slow down 
    # file explorer windows on some operating systems.
    
    download_himawari_data_flat(start_dt, end_dt)