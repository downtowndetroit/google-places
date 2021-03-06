# Google Place Scraper

This script automatically scrape places data using [**Google Place API**](https://developers.google.com/places/web-service/intro) within specific bounding area.

## Install

Clone repository

```
git clone https://github.com/downtowndetroit/google-places.git
```

Change dictionary

```
cd google-places
```

Install required packages
```
conda install pandas numpy requests xlsxwriter
```

## Configeration

In order to let the script perform tasks you want, you need to edit `config.ini` file before running the script. You can use any sublime text editor to edit `config.ini`. Make sure the following parameters are completed and correct:

1. `apikey`: before you run the script, you must fill a valid api key
2. `bounding`: provide bound about the area you are interested in
3. `type`: type of the places you want to scrape, available places are listed [here](https://developers.google.com/places/supported_types)

## Run

After you run this script, the result will be writen to an excel file.

```
python3 placescrape.py OUTPUT_FILE_NAME.xlsx
```
