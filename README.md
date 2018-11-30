
<h1>downtown Detroit Geocoder</h1>

<p><b> Purpose of this geocoder </b></p>

<p>Geocoding and matching user input excel, which contains raw addresses
 in downtown Detroit area to existing reference address table (comprehensive
  downtown Detroit business address table, for test purpose, here we use 
  Melissa Dataset) and rewrite the input table with geocoding output for
   each input addresses</p>

<p> <h2><b> Prerequisite </b></h2></p>

<ol>
<li>edit <code>config.json</code> (with any sublime text editor)
		<ul>
			<li>put <b>absolute path of the input excel table</b> after <code>input_table</code> key in <code>config.json</code> file.</li>
			<li>put <b>absolute path of the output excel table (if exist, will rewrite it)</b> after <code>output_table</code> key in <code>config.json</code> file.</li>
			<li>put <b>absolute path of the reference</b> path after <code>reference_path</code> key in <code>config.json</code> file.</li>
			<li>insert Google API key after googleApiKey key in the config file, the key should support geocode api.</li>
		</ul></li>
	<li>the system should have updated version of python3 with <code>pandas</code>, <code>numpy</code> libraries.</li>
</ol>

**Install Required Packages**
Within Anaconda Environment, intall <code>pandas</code>, <code>numpy</code> using:
<pre><code>conda install pandas numpy
</code></pre>

### config.json Template
<pre><code>{
             "input_table": "YOUR INPUT EXCEL FILE PATH",
             "output_table": "YOUR OUTPUT EXCEL FILE PATH",
             "reference_path" : "THE REFERENCE ADDRESS TABLE PATH",
             "googleApiKey":"THE GOOGLE GEOCODING API KEY",
             "county" : "Wayne County", /* DEFAULT DOWNTOWN DETROIT */
             "state" : "Michigan",
             "viewbox" : "-83.1428,42.3224,-83.0073,42.4068",
             "bound" : "-83.1428,42.3224,-83.0073,42.4068"
           }
</code></pre>
<h2><b> RUN </b></h2>
<p>
after editing the `config.json`, let's run the tool
This application run in the command line. Open terminal 
(or windows command line) and run following commands</p>
<pre><code>$ cd DDP-projects
</code></pre>
<pre><code>$ python geocoder.py
</code></pre>

<h2><b> RESULT </b></h2>

### Output fields:

1. All data in reference Dataset about the input address
2. FLAG: indicate whether or not the output is Geocoded correctly, if
it's not, FLAG will show the reason why it's not accurate 
3. input address 
<br/>

**Sample Result:**

![pic](https://github.com/tianxie1995/DDP-projects/blob/master/ddpresult.png?raw=true) 

<p>Matching reference table appended with Geocoding x, y and potential FLAG</p>

