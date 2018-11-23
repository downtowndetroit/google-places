import pandas as pd
import numpy as np
import requests
import json

'''
Author: Tian Xie
Purpose: This program will geocode address in downtown detroit to specific x,y coordinates

Input: an excel table with address column(s)
ADDITIONAL FIELDS:
1. x,y: longitude and latitude OF the GEOCODing result(came from Google API)
2. flag: indicate whether the geocoder match exact address of the input

System Requirements:
1. Need pandas and numpy libraries
'''

# MAIN PARAMETERS
with open('config.json') as json_data_file:
    data = json.load(json_data_file)
input_table = str(data['input_table'])
output_table = str(data['output_table'])
reference_path = str(data['reference_path'])
googleApiKey = str(data['googleApiKey'])
city = str(data['city'])
county = str(data['county'])
state = str(data['state'])
viewbox = str(data['viewbox'])
bound = str(data['bound'])
ref_data = pd.read_excel(reference_path)  # load reference data


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
    global bound, city, county, state, googleApiKey
    GoogleApiKey = googleApiKey
    params = {'address': '{},{},{}'.format(intersect, city, state),
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
        display_name = False
        x = False
        y = False
    return display_name, x, y


def match_ref(string, df):
    ref_data = df
    prefix = ['East', 'South', 'West', 'North']
    first_word = string.strip().split(',')[0]
    second_word = string.strip().split(',')[1]
    if list(first_word)[0].isdigit() and list(first_word)[-1].isdigit():
        parsed_range_r = first_word
        parsed_name_r = ' '.join(second_word.strip().split(' ')[:-1])
        reg_name = '^({}).*$'.format(parsed_name_r)
        if first_word.strip().split(' ')[0] in prefix:
            parsed_dir_r = first_word.strip().split(' ')[0]
        else:
            parsed_dir_r = False
    else:
        parsed_range_r = False
        parsed_name_r = ' '.join(first_word.strip().split(' ')[:-1])
        reg_name = '^.*\s({}).*$'.format(parsed_name_r)
        if second_word.strip().split(' ')[0] in prefix:
            parsed_dir_r = second_word.strip().split(' ')[0]
        else:
            parsed_dir_r = False

    reg_name = '^.*\s({}).*$'.format(parsed_name_r)
    if parsed_range_r:
        matched_record = ref_data[(ref_data['ParsedRange'] == parsed_range_r)]
        matched_record = matched_record[matched_record['Address'].str.contains(
            reg_name)]
    else:
        matched_record = ref_data[ref_data['Address'].str.contains(reg_name)]
    if parsed_dir_r:
        matched_record = matched_record[(
            ref_data['ParsedPreDir'] == parsed_dir_r)]
    else:
        pass
    return matched_record


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
    matched_record = ref_data[ref_data['Address'].str.contains(reg_name)]
    matched_record['flag'] = flag
    matched_record['x'] = x
    matched_record['y'] = y
    return matched_record


def geocode(address_input):
    global ref_data
    output_df = ref_data[ref_data['Address'] == False]
    for i, address in enumerate(address_input):
        print('Geocoding <{}>...'.format(address))
        google_output, x, y = google_geocode(address)
        if google_output:
            selected_record = google_match_ref(google_output, x, y, ref_data)
            if selected_record.shape[0] > 0:
                selected_record = selected_record.iloc[0]
                output_df = output_df.append(selected_record)
                print('    Complete.')
            else:
                print('    No matching record found in the reference database.', )
                empty_output = ref_data.iloc[0].copy()
                empty_output['flag'] = 'No matching record found in the reference database.'
                empty_output['x'] = x
                empty_output['y'] = y
                output_df = output_df.append(empty_output)
        else:
            print('    Google GeoCoding Error: Address can\'t be found.', )
            empty_output = ref_data.iloc[0].copy()
            empty_output['flag'] = 'Google Address can\'t be found'
            empty_output['x'] = np.nan
            empty_output['y'] = np.nan
            output_df = output_df.append(empty_output)
    return output_df.reset_index()


def main():
    # read input excel table
    global input_table, output_table
    input = pd.read_excel(input_table)
    input_list = input.values.reshape((1, -1))[0]
    output = geocode(input_list)
    output['input_address'] = pd.Series(input_list)
    output.to_excel(output_table, sheet_name="geocoding_output")
    return


if __name__ == '__main__':
    main()
