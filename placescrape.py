'''
Author: Tian Xie
Purpose:

This program will scrape places data from google place API in defined
area.

Parameters:

1. Bounding Box: Setup the south east north west bound of the searching Area
2. Searching Radius: Limit the searching radius for each requests
3. Place type: return places type
'''
import os
import sys
import warnings
import requests
import pandas as pd
import itertools
import time
import config

apikey = config.apikey

south = config.bounding['south']
west = config.bounding['west']
north = config.bounding['north']
east = config.bounding['east']

searchingRadius = config.searchingParameter['searchingRadius']

type = config.searchingParameter['type']

outFolder = config.outputFolder


def scrape(response):
    l = []
    for result in response['results']:
        try:
            placeID = result['place_id']
        except:
            placeID = 'Nan'
        try:
            place_name = result['name']
        except:
            place_name = 'Nan'
        try:
            vicinity = result['vicinity']
        except:
            vicinity = 'Nan'
        try:
            lat = result['geometry']['location']['lat']
            lng = result['geometry']['location']['lng']
        except:
            lat = None
            lng = None
        try:
            place_type1 = result['types'][0]
        except:
            place_type1 = 'Nan'
        try:
            place_type2 = result['types'][1]
        except:
            place_type2 = 'Nan'
        row = (placeID, place_name, vicinity,
               lat, lng, place_type1, place_type2)
        l.append(row)
    return l


def google_place(point, radius, searchType, key):
    dt = []
    GoogleApiKey = key  # enter your api key
    params = {'location': point,
              'radius': radius,
              'type': searchType,
              'key': GoogleApiKey}
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    R = requests.get(url, params=params)
    R.raise_for_status()
    response = R.json()
    print(response['status'])
    # get next_token
    dt = dt + scrape(response)
    # detect if there is another page
    try:
        next_token = response['next_page_token']
    except:
        next_token = False
        print('only 1 page')

    if next_token:
        params = {'key': GoogleApiKey,
                  'pagetoken': next_token}
        time.sleep(2)
        R = requests.get(url, params=params)
        R.raise_for_status()
        response = R.json()
        dt = dt + scrape(response)
        # detect if there is another page
        try:
            next_token = response['next_page_token']
        except:
            next_token = False
            print('only 2 page')
        if next_token:
            params = {'key': GoogleApiKey,
                      'pagetoken': next_token}
            time.sleep(2)
            R = requests.get(url, params=params)
            R.raise_for_status()
            response = R.json()
            dt = dt + scrape(response)
            if len(response['results']) == 20:
                print('Warning: Exceed limit of 60...')
            else:
                pass
        else:
            pass
    else:
        pass
    df = pd.DataFrame(dt, columns=[
                      'placeID', 'name', 'address', 'lat', 'lng',  'primaryType', 'secondaryType'])
    return df


def scanner(south=None, west=None, north=None, east=None, sep=300, searchType='store', apikey=None):
    if south == None or west == None or north == None or east == None:
        sys.exit("Missing Value: Bounding Box needed")
    if apikey == None:
        sys.exit("Missing API key: API key needed")
    search_dist = sep
    lng_diff = float(east) - float(west)
    lat_diff = float(north) - float(south)
    rows = round(lng_diff*111303/search_dist)
    columns = round(lat_diff*110575/search_dist)
    print('Start scraping...')
    print('Your searching Area: ' +
          str(lng_diff*111303) + 'x' + str(lat_diff*110575))
    print('Rows: '+str(rows))
    print('Cols: '+str(columns))
    print('Searching Place Type: ' + searchType)
    lng_unit = lng_diff/columns
    lat_unit = lat_diff/rows
    base_lat = south
    base_lng = west
    x_range = [base_lng+x*lng_unit for x in list(range(1, columns+1, 1))]
    y_range = [base_lat+x*lat_unit for x in list(range(1, rows+1, 1))]
    df = pd.DataFrame(columns=['placeID', 'name', 'address',
                               'lat', 'lng', 'primaryType', 'secondaryType'])
    i = 0
    for y, x in itertools.product(x_range, y_range):
        print(str(x) + ',' + str(y))
        time.sleep(2)
        point = str(x) + ',' + str(y)
        dt = google_place(point, str(search_dist), searchType, apikey)
        df = pd.concat([df, dt], ignore_index=True)
        print(i, df.shape)
        i += 1
    df = df.drop_duplicates(['placeID'])
    return df


def writeExcel(df, path):
    summary = pd.DataFrame({
        'Date': [time.strftime('%m-%d-%Y %H:%M', time.gmtime())],
        'Type': [type],
        'Number of Places': [df.shape[0]]
    })
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    summary.transpose().to_excel(writer, sheet_name='Summary')
    df.to_excel(writer, sheet_name='Data')


def main():
    global apikey, south, west, north, east, searchingRadius, type, outFolder
    df = scanner(south=south,
                 west=west,
                 north=north,
                 east=east,
                 sep=searchingRadius,
                 searchType=type,
                 apikey=apikey)
    output_excel = str(sys.argv[1])
    print(output_excel)
    if (len(output_excel) <= 5):
        warnings.warn(
            'Output excel file path is failed to recognized, use "output.xlsx" instead.', Warning)
        #df.to_excel(os.path.join(outFolder, "output.xlsx"))
        writeExcel(df, os.path.join(outFolder, "output.xlsx"))
    else:
        #df.to_excel(os.path.join(outFolder, output_excel))
        writeExcel(df, os.path.join(outFolder, output_excel))


if __name__ == "__main__":
    main()
