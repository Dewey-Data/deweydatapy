# https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

import geopandas as gpd
import us
# import pandas as pd
# from geopy.geocoders import Nominatim

from ftplib import FTP
import os

# FTP site details
TIGER_FTP_HOST = 'ftp2.census.gov'
TIGER_FTP_DIR_PREFIX = '/geo/tiger/TIGER'

class CensusShape:
    def __init__(self, local_dir, year = None):
        self.local_dir = local_dir
        self.year = year
    def __is_directory(self, ftp, item):
        # Check if the item is a directory
        if '.' in item:
            return False
        else:
            return True
    
        # try:
        #     # Attempt to change directory to the item
        #     ftp.cwd(item)
        #     # If successful, it's a directory
        #     ftp.cwd('..')  # Go back to parent directory
        #     return True
        # except:
        #     # If changing directory fails, it's not a directory
        #     return False
    
    def __census_ftp_login(self, timeout=600):
        # Connect to the FTP server
        ftp = FTP(TIGER_FTP_HOST, timeout=timeout)
        ftp.login()
        return ftp
    
    def __census_ftp_root(self):
        return f'{TIGER_FTP_DIR_PREFIX}{self.year}/'
    
    def __download_shapefiles(self, ftp, ftp_dir, local_dir, skip_existing=False, recursive=False):
        # Change directory to the remote directory
        if ftp_dir.startswith('/'):
            ftp_dir = ftp_dir[1:]
        elif ftp_dir.startswith('./'):
            ftp_dir = ftp_dir[2:]
    
        ftp.cwd(ftp_dir)
    
        # Create the corresponding local directory if it doesn't exist
        local_path = os.path.join(local_dir, ftp_dir)
    
        os.makedirs(local_path, exist_ok=True)
    
        # List files and directories in the remote directory
        files = ftp.nlst()
    
        # Download files and recurse into directories
        for file in files:
            if self.__is_directory(ftp, file):  # if it's a directory
                if recursive:
                    self.__download_shapefiles(ftp, file, local_path, True)
    
            else:  # if it's a file
                local_file = os.path.join(local_path, file)
                # skip if the file already exists
                if skip_existing and os.path.exists(local_file):
                    print(f"Skipping {file} as it already exists in {local_file}")
                    continue
    
                print(f"Downloading {file} to {local_file}")
                with open(local_file, 'wb') as f:
                    ftp.retrbinary('RETR ' + file, f.write)
    
    def download_shapefiles(self, datasets, skip_existing=False, recursive=False, timeout=600):
        # Connect to the FTP server
        ftp = self.__census_ftp_login(timeout=timeout)

        # Download files for each dataset
        if not isinstance(datasets, list):
            datasets = [datasets]
    
        for dataset in datasets:
            # Change directory to the TIGER year root directory
            ftp.cwd(self.__census_ftp_root())
            self.__download_shapefiles(ftp, dataset, self.local_dir, skip_existing, recursive)
    
        # Quit the FTP connection
        ftp.quit()

    # Will be activated later ------------------
    # def geocode_addresses(df, address_column):
    #     """
    #     Adds 'latitude' and 'longitude' columns to the DataFrame based on geocoding the addresses.
    #
    #     Parameters:
    #     - df: A pandas DataFrame containing an address column.
    #     - address_column: The name of the column in the DataFrame that contains the street addresses.
    #
    #     Returns:
    #     - A pandas DataFrame with added 'latitude' and 'longitude' columns.
    #     """
    #
    #     # Initialize Nominatim API
    #     geolocator = Nominatim(user_agent="geo_coder")
    #     # Use rate limiter to avoid hitting service limits
    #
    #     # Define function to apply on each address
    #     def get_geocode(address):
    #         try:
    #             location = geolocator.geocode(address)
    #             return pd.Series((location.latitude, location.longitude))
    #         except AttributeError:
    #             return pd.Series((None, None))
    #
    #     # Apply the function and split the results into two new columns
    #     df[['latitude', 'longitude']] = df[address_column].apply(get_geocode)
    #
    #     return df
    #
    # # # Example usage
    # # data = {
    # #     'address': ['1600 Amphitheatre Parkway, Mountain View, CA', '1 Infinite Loop, Cupertino, CA']
    # # }
    # # df_addresses = pd.DataFrame(data)
    # #
    # # # Geocode addresses
    # # df_geocoded = geocode_addresses(df_addresses, 'address')
    # # print(df_geocoded)
    #
    def read_state_shapefile(self, dataset, state_code):
        # Read the shapefile
        if not state_code.isnumeric():
            state_code = us.states.lookup(state_code).fips
    
        # _state_code_
        state_code_ = f'_{state_code}_'
        local_dir = os.path.join(self.local_dir, dataset)
    
        files = os.listdir(local_dir)
        # Find the shapefile contains state_code_
        file = [file for file in files if state_code_ in file]
        shapefile_path = os.path.join(local_dir, file[0])
    
        gdf = gpd.read_file("zip://" + shapefile_path)
    
        return gdf

    def read_a_shapefile(self, dataset, state_code = None):
        if state_code is not None:
            return self.read_state_shapefile(dataset, state_code)
        else:
            local_dir = os.path.join(self.local_dir, dataset)
            files = os.listdir(local_dir)
            if len(files) == 0:
                print(f"No files found in {local_dir}")
                return None
            elif len(files) > 1:
                print(f"Multiple files found in {local_dir}. Opening the first one.")

            shapefile_path = os.path.join(local_dir, files[0])
            gdf = gpd.read_file("zip://" + shapefile_path)

            return gdf
