
<h1>downtown Detroit Geocoder</h1>

<<<<<<< HEAD
 <h2><b> Prerequisite </b></h2>
  1. edit `config.json` (with any sublime text editor)
	  - put absolute path of the input excel table after `input_table` key in `config.json` file.
	  - put absolute path of the reference path after `reference_path` key in `config.json` file.
	  - insert Google API key after googleApiKey key in the config file, the key should support geocode api.
  2. the system should have updated version of python3 and `pandas`, `numpy` libraries.
=======
<p><b> Purpose of this geocoder </b></p>

<p>geocoding and matching user input excel, which contains raw addresses in downtown Detroit area to existing reference address table (comprehensive downtown Detroit business address table) and rewrite the input table with geocoding output for each input addresses</p>

<p> <h2><b> Prerequisite </b></h2></p>

<ol>
<li>edit <code>config.json</code> (with any sublime text editor)
		<ul>
			<li>put <b>absolute path of the input excel table</b> after <code>input_table</code> key in <code>config.json</code> file.</li>
			<li>put <b>absolute path of the output excel table (if exist, will rewrite it)</b> after <code>output_table</code> key in <code>config.json</code> file.</li>
			<li>put <b>absolute path of the reference</b> path after <code>reference_path</code> key in <code>config.json</code> file.</li>
			<li>insert Google API key after googleApiKey key in the config file, the key should support geocode api.</li>
		</ul></li>
	<li>the system should have updated version of python3 and <code>pandas</code>, <code>numpy</code> libraries.</li>
</ol>
>>>>>>> a105347078dc359e218a0cf823e40592571cf88a

<h2><b> RUN </b></h2>
<p>
after editing the `config.json`, let's run the tool
This application run in the command line. Open terminal</p>
<pre><code>$ cd DDP-projects
</code></pre>
<pre><code>$ python geocoder.py
<<<<<<< HEAD
</code></pre>
=======
</code></pre>

result:
(https://github.com/tianxie1995/DDP-projects/blob/master/ddpresult.png?raw=true) 

<h2><b> RESULT </b></h2>

<p>Matching reference table appended with Geocoding x, y and potential FLAG</p>

 > FLAG appear when the address isn't accurately matching the reference table or GOOGLE API indicate that it doesn't exist.

>>>>>>> a105347078dc359e218a0cf823e40592571cf88a
