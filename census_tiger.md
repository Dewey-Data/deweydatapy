#  Python example for Census mapping.

Many Dewey datasets have geocode information (latitude and longitude).
You may want to join demographics data from Census to your datasets.
This tutorial shows how to download Census TIGER files and join them with Dewey datasets.

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
import pandas as pd
import geopandas as gpd
from census_tiger import *

# Local directory to save downloaded files
# 'C:/tiger/2023' for example
local_dir = 'Your local directory path to save Census TIGER files'
```

To download files for year 2023
```Python
# Download files in the root directory
download_tiger_files(2023, '', local_dir, skip_existing=True)

# Download files in the BG (Block Group) folder
download_tiger_files(2023, ['BG'], local_dir, skip_existing=True)

# Download files in the BG (Block Group), TRACT (Census Tract), CBSA (Core Based Statistical Area) folder
download_tiger_files(2023, ['BG', 'TRACT', 'CBSA'], local_dir, skip_existing=True)
```
`skip_existing` is set to `True` to skip already downloaded files.

Then you can join the Census Tract, Block Group, CBSA, etc. with Dewey datasets.     
```Python
from census_tiger import *
import pandas as pd

```

Direct to the local directory where you saved the Census TIGER files.     
```Python
# Read state shapefile
# 'C:/tiger/2023' for example
local_dir = 'Your local directory path to Census TIGER files'

# Read donwloaded state shapefile
# read_shapefile works only for BG and TRACT filles.
# Reading 'BG' for example. If you know the state code (06 for California, for example), you can use it.
# Or you can use 'CA' instead.
state_bg_gdf = read_shapefile(local_dir, 'BG', '06')
```

You need geocode to spatial join (`sjoin`) the Census TIGER files with Dewey datasets.
Many Dewey datasets have `latitude` and `longitude` columns.

In the following example, I will create a hyphothetical dataset with addresses and geocode them to get latitude and longitude.     
```Python
# Create an example data
addr1 = '1600 Amphitheatre Parkway, Mountain View, California, 94043'
addr2 = '200 N Spring St, Los Angeles, CA 90012'

# Create GeoDataFrame
addr_df = pd.DataFrame({'Address': [addr1, addr2],
                        'latitude': [37.423120361622935, 34.05162175030242],
                        'longitude': [-122.08352124965603, -118.24559360036471]})
```
Now, you can join the Census TIGER files with the Dewey dataset.
`geopandas`'s `sjoin` function is used for the spatial join.      
```Python
addr_gdf = gpd.GeoDataFrame(addr_df, geometry=gpd.points_from_xy(addr_df['longitude'], addr_df['latitude']))

# Spatial join if the address geocode is within the state boundary
joined_gdf = gpd.sjoin(addr_gdf, state_bg_gdf, how='left', predicate='within')
print(joined_gdf)
```

Joined GeoDataFrame will have the columns from both the Dewey dataset and the Census TIGER files
(Census Tract, Block Group, etc.).

![image](https://github.com/Dewey-Data/deweydatapy/assets/142400584/d6b175df-d927-4491-b18f-d1057beaa70f)

CBSA only has one file, `tl_2023_us_cbsa.zip`. In this case, you can open this file directly.
```Python
# Read CBSA shapefile
shapefile_path = r'C:\temp\2023\CBSA\tl_2023_us_cbsa.zip'
cbsa_gdf = gpd.read_file("zip://" + shapefile_path)
```
Then same process afterward.

Thanks,
