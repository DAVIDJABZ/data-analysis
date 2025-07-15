#!/usr/bin/env python
# coding: utf-8

# In[51]:


from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
import pandas as pd
import zipfile
import os


# In[53]:


def download_kaggle_competition_data(competition_name, download_path):
    # Initialize Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Ensure the download path exists
    download_path = Path(download_path)
    if not download_path.exists():
        download_path.mkdir(parents=True, exist_ok=True)

    # Download competition data
    print(f"Downloading data for competition '{competition_name}'...")
    api.competition_download_files(competition_name, path=str(download_path))
    
    # Unzip the competition data
    zip_file = download_path / f"{competition_name}.zip"
    if zip_file.exists():
        print(f"Unzipping {zip_file}...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(download_path)
        zip_file.unlink()  # Optionally delete the zip file after extraction
    else:
        raise FileNotFoundError(f"Zip file {zip_file} not found")

    print(f"Downloaded and extracted data to {download_path}")
    return download_path

def list_csv_files(path):
    # List all CSV files in the given path
    csv_files = list(path.rglob("*.csv"))  # Recursively look for all CSV files
    if csv_files:
        print("Available CSV files:")
        for idx, file in enumerate(csv_files, 1):
            print(f"{idx}. {file.name}")
        return csv_files
    else:
        raise FileNotFoundError("No CSV files found in the dataset folder.")

def load_selected_csv_file(csv_files, file_index):
    # Load the selected CSV file based on the index
    selected_file = csv_files[file_index - 1]  # Convert to 0-based index
    print(f"Loading data from {selected_file}...")
    return pd.read_csv(selected_file)

def load_competition_data(competition_name, download_path):
    # Download the dataset and get the path
    dataset_path = download_kaggle_competition_data(competition_name, download_path)
    
    # List available CSV files and allow the user to select one
    csv_files = list_csv_files(dataset_path)
    file_index = int(input(f"Enter the number of the CSV file you want to load (1-{len(csv_files)}): "))
    
    # Load the selected CSV file into a DataFrame
    return load_selected_csv_file(csv_files, file_index)


# In[55]:


def download_kaggle_data(dataset, dataset_dir):
    """
    Downloads and unzips a Kaggle dataset.

    :param dataset: The Kaggle dataset in 'username/dataset-name' format.
    :param dataset_dir: The directory where the dataset should be stored.
    """
    # Authenticate with Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Create dataset directory if it doesn't exist
    Path(dataset_dir).mkdir(parents=True, exist_ok=True)

    # Download dataset
    print(f"Downloading {dataset}...")
    api.dataset_download_files(dataset, path=dataset_dir, unzip=True)

    print(f"Downloaded and unzipped to {dataset_dir}")


# In[ ]:




