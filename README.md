# downtown Detroit Geocoder

** Purpose of this geocoder **
geocoding and matching user input excel, which contains raw addresses in downtown Detroit area to existing reference address table (comprehensive downtown Detroit business address table) and rewrite the input table with geocoding output for each input addresses

** Prerequisite **
  1. edit `config.json` (with any sublime text editor)
      - put absolute path of the input excel table after `input_table` key in `config.json` file.
      - put absolute path of the reference path after `reference_path` key in `config.json` file.
      - insert Google API key after googleApiKey key in the config file, the key should support geocode api.
  2. the system should have updated version of python3 and `pandas`, `numpy` libraries.

** RUN **
after editing the `config.json`, let's run the tool
This application run in the command line. Open terminal
'' $ cd DDP-projects
'' $ python geocoder.py
