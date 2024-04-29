import os, requests, urllib3, pprint, json, traceback, datetime

class NASA_APIs():
    def downloadPicUrl(self, dir, url, date):
        print('attempting to download image from url: {}'.format(url))
        response = requests.get(url)

        # check response for url call
        if response.status_code == 200:
            # getting path for directory
            directory = os.path.dirname(dir)
            
            # creating directory if it doesn't exist
            if not os.path.exists(dir):
                os.makedirs(dir)
                
            # writing out image
            with open(os.path.join(dir, 'APOD_{}_{}'.format(date, url.split("/")[-1])), 'wb') as outputImage:
                outputImage.write(response.content)

            print('image downloaded')
                
        else:
            print('failed to download image: {}. Status code: {}'.format(url, response.status_code))
    
    def fetchAPOD(self, date, saveImage, dir):
        '''
        Parameter       Type        Default     Description
        date 	        YYYY-MM-DD 	today 	    The date of the APOD image to retrieve
        start_date 	    YYYY-MM-DD 	none 	    The start of a date range, when requesting date for a range of dates. Cannot be used with date.
        end_date 	    YYYY-MM-DD 	today 	    The end of the date range, when used with start_date.
        count 	        int 	    none 	    If this is specified then count randomly chosen images will be returned. Cannot be used with date or start_date and end_date.
        thumbs 	        bool 	    False 	    Return the URL of video thumbnail. If an APOD is not a video, this parameter is ignored.
        api_key 	    string 	    DEMO_KEY 	api.nasa.gov key for expanded usage
        '''
        URL_APOD = "https://api.nasa.gov/planetary/apod"
        params = {
            'api_key':self.apiKey,
            'date':date,
        }
        response = requests.get(URL_APOD,params=params).json()
        pprint.PrettyPrinter().pprint(response)

        if saveImage:
            self.downloadPicUrl(dir, response['hdurl'], date)
        
    def __init__(self):
        # NASA unq api key
        self.apiKey = '0aa2HF50BeZ76DJGoklPqf0t7HqfK1ZsF4rgu0uC'
        
        self.todayYYYYMMDD = datetime.datetime.now().strftime("%Y-%m-%d")