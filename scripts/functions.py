""" commonly used function here 


CPCB FORMAT: 15Min_2017_site_168_Bandra_Mumbai_MPCB_15Min.csv
req        : Raw_data_15Min_2019_site_5112_Powai_Mumbai_MPCB_15Min.csv
"""
def get_siteId_Name_Year_City(file: str, sites: list):
    """
    Extracts site_id, site_name, year, and city from the filename based on its format.
    
    Args:
    - file (str): The filename to extract information from.
    - sites (list): A list or DataFrame containing site details, including 'site_code' and 'city'.

    Returns:
    - tuple: (site_id, site_name, year, city)
    """
    
    if file.lower().startswith("15min"):
        parts = file.split('_')
        year = int(parts[1])                 # Year is the second part
        site_id = '_'.join(parts[2:4])       # Site ID is the third and fourth parts
        site_name = '_'.join(parts[4:-1]).replace(".csv", "")  # Site name is between the 5th element and the end minus .csv
        
    elif file.lower().startswith("raw_data"):
        parts = file.split('_')
        year = int(parts[3])                 # Year is the fourth part
        site_id = '_'.join(parts[4:6])       # Site ID is the fifth and sixth parts
        site_name = '_'.join(parts[6:-1]).replace(".csv", "")  # Site name starts from the seventh part

    else:
        raise ValueError("Filename format is not recognized")

    city_data = sites[sites['site_code'] == site_id]['city']
    if not city_data.empty:
        city = city_data.values[0].strip()  # Extract and strip whitespace from city name
    else:
        city = "Unknown"  # Handle cases where site_id is not found in the sites DataFrame

    print(f"SITE ID: {site_id} - SITENAME: {site_name} - YEAR: {year} - CITY: {city}")
    return site_id, site_name, year, city


