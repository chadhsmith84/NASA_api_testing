# NASA_api_testing
- written with python 3.12
- dependencies [os, requests, urllib3, json, datetime, traceback, getopt, sys]
- config with unq api key from NASA is excluded from repository
	- navigate to https://api.nasa.gov/
	- fill out the form to generate unq api key free of charge
	- update line 50 in APIs.py to your unique api key or add as an environment variable
		-         params = {
				'api_key':'myUnqKeyFromNASA',
				'date':date,
				}

# Showing ability to work with API calls from NASA and parse JSON
- from command line
	- c:\python312\python.exe "PathToPythonFile\NASA_api_testing.py" --date YYYY/MM/DD
		- The --date paramater is optional. If not todays date will be used
			- applicaiton will error if date is not between 06/19/1995 and Today
				- images were not stored prior to this date
		- This will call the fetchAPOD function to download the APOD (Astronomy Picture of the Day) to PathToPythonFile\NASA_api_testing.py in a subdirectory "APOD_Images"
		- https://apod.nasa.gov/apod/astropix.html
		- returned JSON data is parsed and logged/displayed