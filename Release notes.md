# Releaes notes

## 0.2.0
- Add a new function `get_meta` to get meta data
- Changed the download way to three steps
  - Get meta to check date range
  - Get download link (`files_df`) for specific date range
  - Download files
- `skip_exists` default is `FALSE`
