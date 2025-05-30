# Releaes notes

## 0.3.0
- Fixed the API to work with the new beta platform (https://platform.deweydata.io)

## 0.2.1
- Added function `download_files1`

## 0.2.0
- Added a new function `get_meta` to get meta data
- Changed the download way to three steps
  - Get meta to check date range
  - Get download link (`files_df`) for specific date range
  - Download files
- `skip_exists` default is `False`
