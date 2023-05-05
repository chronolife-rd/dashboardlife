# Dashboard Life

<h2> Architecture </h2>
<h3>Root</h3>
<ul>
  <li>.gitignore</li>
  <li>README.md</li>
  <li>home.py: main file</li>
  <li>requirements.txt: list of packages name and version</li>
</ul>

<h3>.streamlit/config.toml</h3>
<p>Global config of streamlit</p>

<h3>data/</h3>
<p>Copy of the github repository "garmin_automatic_reports" maintained by the Data Scientist team to request data using the REST API</p>

<h3>pylife/</h3>
<p>Copy of the github repository "pylife" maintained by the Data Scientist team to manage data (to be cleaned by the Data Science team)</p>

<h3>template/</h3>
<p>This folder contains a list of scripts to manage the core of this streamlit app</p>
<ul>
  <li>images/ : store all images</li>
  <li>languages/ : manage languages</li>
  <li>contant.py : store all constants of the project</li>
  <li>css.py : custom styles</li>
  <li>data_controller.py : control data comming from the <i>data/</i> folder</li>
  <li>display.py : main file for displaying with streamlit methods </li>
  <li>download.py : parse data and create downloadable file for streamlit </li>
  <li>html.py : custom html </li>
  <li>session.py : manage global variables and session data (language, images, etc.)</li>
  <li>test.py : test form fields and user authentication</li>
  <li>util.py : useful functions</li>
  <li>version.py : project versionning</li>
</ul>
