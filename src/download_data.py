import os
import urllib.request
import pandas as pd

def download_nyc_tlc_data():
    # مسیر ذخیره فایل
    data_dir = os.path.join("data", "raw")
    os.makedirs(data_dir, exist_ok=True)
    
    # لینک دانلود داده‌های ژانویه ۲۰۲۴
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    file_path = os.path.join(data_dir, "yellow_tripdata_2024-01.parquet")
    
    if not os.path.exists(file_path):
        print(f"Downloading data from {url}...")
        urllib.request.urlretrieve(url, file_path)
        print("Download complete!")
    else:
        print("File already exists. Skipping download.")
        
    # یک پیش‌نمایش از داده بگیریم
    print("Loading a sample of the data...")
    df = pd.read_parquet(file_path)
    print(f"Data shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nColumns and Types:")
    print(df.dtypes)

if __name__ == "__main__":
    download_nyc_tlc_data()