# deweydataypy
**_Python_** API for Dewey Data Inc. Currently supports file download and utility functions.

Find the release notes here: [Release Notes](https://github.com/Dewey-Data/deweydatapy/blob/main/Release%20notes.md).

Bug report: https://community.deweydata.io/c/help/python/43.

Explore data at https://www.deweydata.io/.

# API tutorial
### 1. Create API Key
In the system, click Connections → Add Connection to create your API key.

<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/8ba869f0-3356-439c-8288-8b8d4bb76326" width="800">
<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/f479586b-ccf4-490b-852c-90051b1e7008" width="600">

As the message says, please make a copy of your API key and store it somewhere. Also, please hit the **Save** button before use.

### 2. Get a product path
Choose your product and Get / Subscribe → Connect to API then you can get API endpoint (product path). Make a copy of it.
<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/77000d10-3e36-42c8-be36-361e30e76017" width="800">

### 3. Install `deweydatapy` library
You can install this library directly from the GitHub source as following.
```Python
pip install deweydatapy@git+https://github.com/Dewey-Data/deweydatapy
```
If you use PyCharm, [Python Packages] → [Add Package] → [From Version Control] → Select [Git] and input
```Python
https://github.com/Dewey-Data/deweydatapy
```

```Python
# Use deweydatapy library
import deweydatapy as ddp
```

`deweydatapy` package has the following functions:
* `get_meta`: gets meta information of the datset, especially date range as returned in a `dict`
* `get_file_list`: gets the list of files in a `DataFrame`
* `download_files`: download files from the file list to a destination folder
* `download_files0`: download files with apikey and product path to a destination folder
* `read_sample`: read a sample of data for a file download URL
* `read_sample0`: read a sample of data for the first file with apikey and product path
* `read_local`: read data from locally saved csv.gz file

### 4. Examples
I am going to use Advan weekly pattern as an example.
```Python
import deweydatapy as ddp

# API Key
apikey_ = "Paste your API key from step 1 here."

# Advan product path
pp_advan_wp = "Paste product path from step 2 here."
```
You will only have one API Key while having different product paths for each product.

As a first step, check out the meta information of the dataset by
```Python
meta = ddp.get_meta(apikey_, pp_advan_wp, print_meta = True);
```
This will return a `DataFrame` with meta information. `print_meta = True` will print the meta information.
<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/ce75f4ff-87a2-4034-8eaf-8474d0b2f96a" width = "600">

You can see that the data has a partition column `DATE_RANGE_START`. Dewey data is usally huge and the data will be partitioned by this column into multiple files. We can also see that the minimum data available date is `2018-01-01` and maximum data available date is `2024-01-08`.
After checking this, I will download data between `2023-09-03` and `2023-12-31`.

Next, collect the list of files to download by
```Python
files_df = ddp.get_file_list(apikey_, pp_advan_wp, 
                             start_date = '2023-09-03',
                             end_date = '2023-12-31',
                             print_info = True);
```
If you do not specifiy `start_date`, it will collect all the files from the minimum available date, and do not spesify `end_date`, all the files to the maximum available date.

**Dewey datasets are very large most of the time. Please specify `start_date` and `end_date`.**

`print_info = True` set to print another meta information of the files like below:
<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/01f12591-132d-4e2d-8cf6-9927f58c610a" width = "600">

files_df has a file links (`DataFrame`) with the following information:
* `index`: file index ranges from 1 to the number of files
* `page`: page of the file
* `link`: file download link
* `partition_key`: to subselect files based on date
* `file_name`
* `file_extension`
* `file_size_bytes`
* `modified_at`

Finally, you can download the data to a local destination folder by
```Python
ddp.download_files(files_df, "C:/Temp", skip_exists = True)
```
This will download files to `C:/Temp` directory, with the following progress messages.
<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/3fe96208-1f96-4d6f-a360-9ca5ace99d57" width = "800">

If you attempt to download all the files again and want to skip already existing downloaded files, set `skip_exists = True`. The default value is set to `False` (the default value was `True` in versions 0.1.x).

You can also use `filename_prefix` option to give file name prefix for all the files. For example, following will save all the files in the format of `advan_wp_xxxxxxx.csv.gz`.


```Python
ddp.download_files(files_df, "C:/Temp", filename_prefix = "advan_wp_", skip_exists = True)
```

Alternatively, you can download files skipping `get_file_list` by
```Python
ddp.download_files0(apikey_, pp_advan_wp, "C:/Temp",
                    start_date = '2023-09-03', end_date = '2023-12-31')
```

Some datasets do not have partition column as they are time invariant (SafeGraph Global Places (POI) & Geometry, for example).
```Python
meta = ddp.get_meta(apikey_, pp_sg_poipoly, print_meta = True);
```
<img src="https://github.com/Dewey-Data/deweydatapy/assets/142400584/cfea2339-5386-4083-a4e6-7cc89a9ba284" width = "600">

There is no partition column and minimum and maximum dates are not available. In that case, you can download the data without specifiying date ranges.
 
```Python
files_df = ddp.get_file_list(apikey_, pp_sg_poipoly, print_info = True);
```
<br><br>
You can quickly load/see a sample data by
```Python
sample_df = ddp.read_sample(files_df['link'][0], nrows = 100)
```
This will load sample data for the first file in `files_df (files_df['link'][0])` for the first 100 rows. You can see any files in the list.

You can also see the sample of the first file by
```Python
sample_data = ddp.read_sample0(apikey_, pp_advan_wp, nrows = 100);
```
This will load the first 100 rows for the first file of Advan data.

You can open a downloaded local file (a csv.gz or csv file) by
```Python
sample_local = ddp.read_local("C:/Temp/Weekly_Patterns_Foot_Traffic_Full_Historical_Data-0-DATE_RANGE_START-2023-09-04.csv.gz",
                              nrows = 100)
```

Thanks
