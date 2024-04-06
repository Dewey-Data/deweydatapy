#  Python example for Census mapping.

Many Dewey datasets have geocode information (latitude and longitude).
You may want to join demographics data from Census to your datasets.
This tutorial shows how to download Census TIGER files and join them with Dewey datasets.
------------------------

Census provides TIGER files for mapping (https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html).
You can download the files from the Census FTP server.
The following code snippet shows how to download the files then use it with Dewey datasets.


First please download the `census_tiger.py` file from the following link:
*https://github.com/Dewey-Data/deweydatapy/blob/main/deweydatapy/census_tiger.py*
(This is not a part of the Dewey dataset package yet.)

The Censuf FTP has files/folders like below.
You can download all of them or specific files/folders in the following way.
<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/78ede7bb-b889-4ca1-835f-c65070430d68" width = "400">

Initiate the FTP server connection.
```Python
# Census TIGER FTP download code sample ----------------------
from census_tiger import *

# Local directory to save downloaded files
local_dir = 'Your local directory path to save Census TIGER files'

# Connect to the FTP server first
ftp = census_ftp_login()

```

You can download files in an FTP folder to the local directory
```Python
# First, you have to move to the root directory before downloading new folder
# Move to 2023 Census TIGER files root directory
ftp.cwd(census_ftp_root(2023))
# Downloand Census Block Group shape files
download_files(ftp, 'BG', local_dir)

# First, you have to move to the root directory before downloading new folder
# Move to 2023 Census TIGER files root directory
ftp.cwd(census_ftp_root(2023))
# Downloand Census Tract shape files
download_files(ftp, 'TRACT', local_dir)
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
Many Dewey datasets have `latitude` and `longitude` columns.

In the following example, I will create a hyphothetical dataset with addresses and geocode them to get latitude and longitude.     
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

Joined GeoDataFrame will have the columns from both the Dewey dataset and the Census TIGER files
(Census Tract, Block Group, etc.).

![image](https://github.com/Dewey-Data/deweydatapy/assets/142400584/ea40f5f1-333b-47e6-9cdf-057975c9797e)

Row number 3 has correct Census Tract and Block Group information.

Thanks,
