# downtown Detroit Geocoder

~<b>~ Purpose of this geocoder ~</b>~
geocoding and matching user input excel, which contains raw addresses in downtown Detroit area to existing reference address table (comprehensive downtown Detroit business address table) and rewrite the input table with geocoding output for each input addresses

~~ <h2><b> Prerequisite </b></h2>
  1. edit `config.json` (with any sublime text editor)
	  - put absolute path of the input excel table after `input_table` key in `config.json` file.
	  - put absolute path of the reference path after `reference_path` key in `config.json` file.
	  - insert Google API key after googleApiKey key in the config file, the key should support geocode api.
  2. the system should have updated version of python3 and `pandas`, `numpy` libraries.

~~ <h2><b> RUN </b></h2>
~~ <p>
~~ after editing the `config.json`, let's run the tool
~~ This application run in the command line. Open terminal</p>
~~ <pre><code>$ cd DDP-projects
~~ </code></pre>
~~ <pre><code>$ python geocoder.py
~~ </code></pre>
