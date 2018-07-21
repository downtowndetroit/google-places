import pandas as pd #python data science toolkit: data manipulation and database maneging
import numpy as np #mathematic function
import requests #api
import re #regex sytax

'''
Author: Tian Xie 
Purpose: This program will geocode address in downtown detroit to specific x,y coordinates 

Input: table with address column(s)
ADDITIONAL FIELDS: 
1. x,y: longitude and latitude OF the GEOCODing result(came from Google API)
2. flag: indicate whether the geocoder match exact address of the input 

System Requirements: 
1. Need pandas and numpy libraries
'''

# MAIN PARAMETERS
data_file = 'data/Washtenaw+County+Ride+Sharing+Research+Survey_June+26%2C+2018_14.17.csv'  # PUT THE DATA FILE HERE
county = 'Wayne County'
state = 'Michigan'
viewbox = '-83.1428,42.3224,-83.0073,42.4068'
bound = '-83.1428,42.3224,-83.0073,42.4068'


def OSM_geocode(address):
    url = 'https://nominatim.openstreetmap.org/search'
    global county, state, viewbox
    params = {'q': address,
              'county': county,
              'state': state,
              'viewbox': viewbox,
              'bounded': 1,
              'format': 'json',
              'addressdetails': 0,
              'countrycodes': 'US'}
    try:
        R = requests.get(url, params=params)
        R.raise_for_status()
        response = R.json()
        display_name = response[0]['display_name']
    except:
        display_name = google_geocode(address)

    return display_name


def google_geocode(intersect):
    global bound, county
    GoogleApiKey = 'AIzaSyA_AwST7YZY19TyJOp9L6VXJzBimg4LgVw'  # enter your api key
    params = {'address': intersect + ', ' + county,
              'bounds': bound,
              'key': GoogleApiKey}
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    R = requests.get(url, params=params)
    R.raise_for_status()
    response = R.json()
    try:
        display_name = response['results'][0]['formatted_address']
        x = response['results'][0]['geometry']['location']['lng']
        y = response['results'][0]['geometry']['location']['lat']
    except:
        display_name, x, y = False
    return display_name, x, y


def match_ref(string, df):
    ref_data = df
    prefix = ['East', 'South', 'West', 'North']
    first_word = string.strip().split(',')[0]
    second_word = string.strip().split(',')[1]
    if list(first_word)[0].isdigit() and list(first_word)[-1].isdigit():
        parsed_range_r = first_word;
        parsed_name_r = ' '.join(second_word.strip().split(' ')[:-1]);
        reg_name = '^({}).*$'.format(parsed_name_r)
        if first_word.strip().split(' ')[0] in prefix:
            parsed_dir_r = first_word.strip().split(' ')[0];
        else:
            parsed_dir_r = False
    else:
        parsed_range_r = False
        parsed_name_r = ' '.join(first_word.strip().split(' ')[:-1]);
        reg_name = '^.*\s({}).*$'.format(parsed_name_r);
        if second_word.strip().split(' ')[0] in prefix:
            parsed_dir_r = second_word.strip().split(' ')[0];
        else:
            parsed_dir_r = False

    reg_name = '^.*\s({}).*$'.format(parsed_name_r)
    if parsed_range_r:
        matched_record = ref_data[(ref_data['ParsedRange'] == parsed_range_r)];
        matched_record = matched_record[matched_record['Address'].str.contains(reg_name)];
    else:
        matched_record = ref_data[ref_data['Address'].str.contains(reg_name)];
    if parsed_dir_r:
        matched_record = matched_record[(ref_data['ParsedPreDir'] == parsed_dir_r)];
    else:
        pass
    return matched_record;


def google_match_ref(string, x, y, df):
    ref_data = df
    flag = None
    first_word = string.strip().split(',')[0]
    first_word_1st_word = first_word.strip().split(' ')[0]
    second_word = string.strip().split(',')[1]
    if list(first_word_1st_word)[0].isdigit() and list(first_word_1st_word)[-1].isdigit():
        parsed_address = ' '.join(first_word.strip().split(' ')[:-1])
        reg_name = '^({}).*$'.format(parsed_address)
    else:
        if list(second_word.strip().split(' ')[0])[0].isdigit() and list(second_word.strip().split(' ')[0])[
            -1].isdigit():
            parsed_address = ' '.join(second_word.strip().split(' ')[:-1])
            reg_name = '^({}).*$'.format(parsed_address)
        else:
            flag = 'Do not match exact address.'
            parsed_address = ' '.join(second_word.strip().split(' ')[:-1])
            reg_name = '^.*({}).*$'.format(parsed_address)
    matched_record = ref_data[ref_data['Address'].str.contains(reg_name)];
    matched_record['flag'] = flag
    matched_record['x'] = x
    matched_record['y'] = y
    return matched_record;


def geocode(address_input):
    global ref_data
    output_df = ref_data[ref_data['Address'] == False]
    for i, address in enumerate(address_input):
        # disable OSM geocoder
        if None:  # list(address)[0].isdigit():
            print('Geocoding <{}>...'.format(address))
            OSM_output = OSM_geocode(address)
            selected_record = match_ref(OSM_output, ref_data)
            if selected_record.shape[0] > 0:
                selected_record = selected_record.iloc[0]
                output_df = output_df.append(selected_record)
                print('    Complete.')
            else:
                print('    OSM Address cant be found.')
                print('    Trying Google API... ')
                google_output = google_geocode(address)
                selected_record = google_match_ref(google_output, ref_data)
                if selected_record.shape[0] > 0:
                    selected_record = selected_record.iloc[0]
                    output_df = output_df.append(selected_record)
                    print('    Complete.')
                else:
                    print('    Google Address cant be found.')
        else:
            print('Geocoding <{}>...'.format(address))
            google_output, x, y = google_geocode(address)
            selected_record = google_match_ref(google_output, x, y, ref_data)
            if selected_record.shape[0] > 0:
                selected_record = selected_record.iloc[0]
                output_df = output_df.append(selected_record)
                print('    Complete.')
            else:
                print('    Google Address cant be found.', )
    return output_df.reset_index()

ref_data = pd.read_excel('Documents/DDP/data/3930806-RS.xlsx') #load reference data
