# deweydataypy

**_Python_** example for Census mapping.

Census provides TIGER files for mapping (https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html).
You can download the files from the Census FTP server.
The following code snippet shows how to download the files then use it with Dewey datasets.


First please download the `census_tiger.py` file from the following link:
*https://github.com/Dewey-Data/deweydatapy/blob/main/deweydatapy/census_tiger.py*
(This is not a part of the Dewey dataset package yet.)

The Censuf FTP has files/folders like below.
You can download all of them or specific files/folders in the following way.

![img_1.png](img_1.png)

Initiate the FTP server connection and move to the root directory of the year 2023.
```Python
# Census TIGER FTP download code sample ----------------------
# Local directory to save downloaded files
local_dir = 'Your local directory path to save Census TIGER files'

# Connect to the FTP server first
ftp = census_ftp_login()

# Change directory to the year 2023 TIGER directory
ftp.cwd(census_ftp_root(2023))
```

You can download files in an FTP folder to the local directory (not recommended)     
```Python
# First, you have to move to the root directory before downloading new folder
ftp.cwd(census_ftp_root(2023))
# Downloand Census Block Group shape files
download_files(ftp, 'BG', local_dir, recursive=True)

# First, you have to move to the root directory before downloading new folder
ftp.cwd(census_ftp_root(2023))
# Downloand Census Tract shape files
download_files(ftp, 'TRACT', local_dir, recursive=True)
```

**Not recommended** but you can download all files from the FTP server, recursively.     
```Python
# Download all.
# First, you have to move to the root directory before downloading new folder
ftp.cwd(census_ftp_root(2023))
# Downloand all files recursively
download_files(ftp, '', local_dir, recursive=True)
```

Please quit the FTP server after downloading all the files.     
```Python
# Quit FTP
ftp.quit()
```

Then you can join the Census Tract, Block Group, CBSA, etc. with Dewey datasets.     
```Python
from census_tiger import *
import pandas as pd
```

Direct to the local directory where you saved the Census TIGER files.     
```Python
# Read state shapefile
local_dir = 'Your local directory path to Census TIGER files'

# If you know the state code (06 for California, for example), you can use it.
# Or you can use 'CA' instead.
state_code = '06'

# Read donwloaded state shapefile
# read_shapefile works only for BG and TRACT filles.
state_gdf = read_shapefile(root_dir, state_code)
```

You need geocode to spatial join (`sjoin`) the Census TIGER files with Dewey datasets.
Many Dewey datasets have latitude and longitude columns.

In the following example, we will create a hyphothetical dataset with addresses and geocode them to get latitude and longitude.     
```Python
# Create an example data
addr1 = '1600 Amphitheatre Parkway, Mountain View, California, 94043'
addr2 = '1 Apple Park Way, Cupertino, California, 95014'
addr3 = '200 N Spring St, Los Angeles, CA 90012'

# Create GeoDataFrame
addr_df = pd.DataFrame({'Address': [addr1, addr2, addr3]})

# Add geocode
addr_df = geocode_addresses(addr_df, 'Address')
```

`geocode_addresses` uses `geopy` to geocode the addresses. `addr3` is Los Angeles City Hall.
I found that the latitude and longitude of the City Hall from `geopy` is inaccurate.
So, the following row is added to the DataFrame manually.     
```Python
new_row = pd.DataFrame({'Address': [addr3],
                        'latitude': [34.05162175030242],
                        'longitude': [-118.24559360036471]})

addr_df = pd.concat([addr_df, new_row], ignore_index=True)
```

Now, you can join the Census TIGER files with the Dewey dataset.     
```Python
addr_gdf = gpd.GeoDataFrame(addr_df, geometry=gpd.points_from_xy(addr_df['longitude'], addr_df['latitude']))

joined_gdf = gpd.sjoin(addr_gdf, state_gdf, how='left', predicate='within')
print(joined_gdf)
```

Joined GeoDataFrame will have the columns from both the Dewey dataset and the Census TIGER files.
![img_2.png](img_2.png)

Thanks,