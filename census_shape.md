#  Python example for Census mapping.

**This module is being developed. Your feedback is welcome.**

Many Dewey datasets have geocode information (latitude and longitude).
You may want to join demographics data from Census to your datasets.
This example shows how to download Census shapefiles and join them with Dewey datasets.

Census provides shapefiles for mapping (https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html).
You can download the files from the Census FTP server.
The following code snippet shows how to download the files then use it with Dewey datasets.


First please download the `census_shape.py` file from the following link:
*https://github.com/Dewey-Data/deweydatapy/blob/main/deweydatapy/census/census_shape.py*
(This is not a part of the Dewey dataset package yet.)

The Census FTP has files/folders like below.
You can download all of them or specific files/folders in the following way.
<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/78ede7bb-b889-4ca1-835f-c65070430d68" width = "400">

Import necessary libraries and the `census_shape.py` file.
 Also, prepare local directory to save Census shape files.
```Python
# Census shapefile FTP download code sample ----------------------
import pandas as pd
import geopandas as gpd
from census_shape import *

# Local directory to save downloaded files
# 'C:/census_shape/2023' for example
local_dir = 'Your local directory path to save Census shapefiles'
```

To download files for year 2023, you can use any of the following approches.
```Python
# Download files in the root directory
# Create a CensusShape object
cs = CensusShape(local_dir, 2023)

# Download files in the root directory
cs.download_shapefiles('', skip_existing=True, timeout=600)

# Download shapefiles for a specified dataset
cs.download_shapefiles(['CSA'], skip_existing=True)

# Download shapefiles for the specified datasets
cs.download_shapefiles(['BG', 'TRACT', 'CBSA'], skip_existing=True)
```
`skip_existing` is set to `True` to skip already downloaded files. `timeout` is set to 600 seconds. You can
increase `timeout` if you have a slow internet connection.

Then you can join the Census Tract, Block Group, CBSA, etc. with Dewey datasets. Direct to the local directory where
you saved the Census shapefiles.     
```Python
# Read state shapefile

# Read donwloaded state shapefile
# read_shapefile works only for BG and TRACT filles.
# Reading 'BG' for example. If you know the state code (06 for California, for example), you can use it.
# Or you can use 'CA' instead.
# Below will read 'C:/census_shape/2023/BG/tl_2023_06_bg.zip' file.
state_bg_gdf = cs.read_state_shapefile('BG', '06')
```

You need geocode to spatial join (`sjoin`) the Census shapefiles with Dewey datasets.
Many Dewey datasets have `latitude` and `longitude` columns.

In the following example, I will create a hyphothetical dataset with addresses and geocode them to get latitude and longitude.     
```Python
# Create an example data
addr1 = '1600 Amphitheatre Parkway, Mountain View, California, 94043'
addr2 = '200 N Spring St, Los Angeles, CA 90012'

# Create address DataFrame
addr_df = pd.DataFrame({'Address': [addr1, addr2],
                        'latitude': [37.423120361622935, 34.05162175030242],
                        'longitude': [-122.08352124965603, -118.24559360036471]})

# Convert to a GeoDataFrame
addr_gdf = gpd.GeoDataFrame(addr_df, geometry=gpd.points_from_xy(addr_df['longitude'], addr_df['latitude']))
```
Now, you can join the Census shapefiles with the Dewey dataset.
`geopandas`'s `sjoin` function is used for the spatial join.
This will spatial join if the address geocode is within the state_bg_gdf boundary (polygon of BG, TRACT, CBSA, etc.)

```Python
# Spatial join if the address geocode is
# within the state_bg_gdf boundary (polygon of BG, TRACT, CBSA, etc.)
joined_gdf = gpd.sjoin(addr_gdf, state_bg_gdf, how='left', predicate='within')
print(joined_gdf)
```

Joined GeoDataFrame will have the columns from both the Dewey dataset and the Census shapefiles
(Census Tract, Block Group, etc.).

![image](https://github.com/Dewey-Data/deweydatapy/assets/142400584/d6b175df-d927-4491-b18f-d1057beaa70f)

CBSA only has one file, `tl_2023_us_cbsa.zip`. In this case, you can read it by
```Python
# Read CBSA shapefile
cbsa_gdf = cs.read_a_shapefile('CBSA')
```
or you can open this file directly using GeoDataFrame.
```Python
# Read CBSA shapefile
shapefile_path = r'C:\census_shape\2023\CBSA\tl_2023_us_cbsa.zip'
# Read CBSA shapefile as GeoDataFrame
cbsa_gdf = gpd.read_file("zip://" + shapefile_path)
```
Then same process afterward.

Once you have Census data, such as American Community Survey (ACS)
(https://www.census.gov/programs-surveys/acs), you can join them with Dewey datasets
by Census Tract or Glock Group.

If you are interested in more detailed census data operations, you may consider exploring
libraries such as `pygris` (https://walker-data.com/pygris/) and
`ceppy` (https://cenpy-devs.github.io/cenpy/).

Thanks,
