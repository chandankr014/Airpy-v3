import os
import pandas as pd



def save_to_directory(folder=".TEMP", file=None):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file)
    return file_path


def get_year_int(dates):
    dates = pd.to_datetime(dates, errors='coerce')
    return dates.dt.year

