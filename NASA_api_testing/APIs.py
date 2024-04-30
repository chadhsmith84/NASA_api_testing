import os, requests, urllib3, json, datetime
# import pprint
import config
from log import Logger

class NASA_APIs():
    def try_parsing_date(self, text):
        for fmt in ('%Y%m%d', '%Y-%m-%d','%Y/%m/%d', '%m%d%Y', '%m/%d/%Y', '%m-%d-%Y'):
            try:
                return datetime.datetime.strptime(text, fmt).date().strftime('%Y-%m-%d')
            except ValueError:
                pass
        raise ValueError('no valid date format found')
        
    def downloadPicUrl(self, dir, url, date):
        self.log.info('attempting to download image from url: {}'.format(url))
        response = requests.get(url)

        # check response for url call
        if response.status_code == 200:
            # getting path for directory
            directory = os.path.dirname(dir)
            
            # creating directory if it doesn't exist
            if not os.path.exists(dir):
                os.makedirs(dir)
                
            # writing out image
            downloadPath = os.path.join(dir, 'APOD_{}_{}'.format(date, url.split("/")[-1]))                
            with open(downloadPath, 'wb') as outputImage:
                outputImage.write(response.content)

            self.log.info('image downloaded to {}'.format(downloadPath))
                
        else:
            self.log.info('failed to download image: {}. Status code: {}'.format(url, response.status_code))
    
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

        self.log.info('Running APOD (Astronomy Pricture of the Day) for date: {}'.format(date))
        
        URL_APOD = "https://api.nasa.gov/planetary/apod"
        params = {
                'api_key':config.apiKey,
                'date':date,
                }
        try:         
            response = requests.get(URL_APOD,params=params)#.json()
            response.raise_for_status()
            
        except requests.RequestException as e:
            self.log.critical(response.text)
            raise ValueError(e)

        # pprint.PrettyPrinter().pprint(response)

        if saveImage:
            self.downloadPicUrl(dir, response['hdurl'], date)
        
    def __init__(self):        
        self.todayYYYYMMDD = datetime.datetime.now().strftime("%Y-%m-%d")

        self.log = Logger(os.path.join(os.getcwd(), 'log', datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.log'))