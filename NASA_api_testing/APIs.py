import os, requests, urllib, json, datetime
import webbrowser
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

    def openImage(self, img):
        self.log.info('opening image: {}'.format(img))
        os.startfile(img)

    def openUrl(self, url):
        '''
        If new is 0, the url is opened in the same browser window if possible. 
        If new is 1, a new browser window is opened if possible. 
        If new is 2, a new browser page ("tab") is opened if possible
        '''
        self.log.info('opening url: {}'.format(url))

        # checking url is valid
        response = urllib.request.urlopen(url)

        # opening url if it is valid
        if response.status == 200:
            webbrowser.open(url, new = 0)
        else:
            raise ValueError('received response: {}, reason: {} for url: {}'.format(response.status, response.reason, response.url))

    def downloadPicUrl(self, dir, url, date):
        self.log.info('attempting to download image from url: {}'.format(url))
        response = requests.get(url)

        # check response for url call
        if response.status_code == 200:

            # creating directory if it doesn't exist
            if not os.path.exists(dir):
                os.makedirs(dir)
                
            # defining download path
            downloadPath = os.path.join(dir, 'APOD_{}_{}'.format(date, url.split("/")[-1]))

            # writing out image
            with open(downloadPath, 'wb') as outputImage:
                outputImage.write(response.content)

            self.log.info('image downloaded to {}'.format(downloadPath))

            return downloadPath
                
        else:
            self.log.info('failed to download image: {}. Status code: {}'.format(url, response.status_code))
    
    #def fetchAPOD(self, date, saveImage, dir):
    def fetchAPOD(self, **kwargs):
        try:
            '''
            Parameter       Type        Default     Description
            date 	        YYYY-MM-DD 	today 	    The date of the APOD image to retrieve
            start_date 	    YYYY-MM-DD 	none 	    The start of a date range, when requesting date for a range of dates. Cannot be used with date.
            end_date 	    YYYY-MM-DD 	today 	    The end of the date range, when used with start_date.
            count 	        int 	    none 	    If this is specified then count randomly chosen images will be returned. Cannot be used with date or start_date and end_date.
            thumbs 	        bool 	    False 	    Return the URL of video thumbnail. If an APOD is not a video, this parameter is ignored.
            api_key 	    string 	    DEMO_KEY 	api.nasa.gov key for expanded usage
            '''

            self.log.info('Running APOD (Astronomy Pricture of the Day) for date: {}'.format(kwargs['date']))
        
            URL_APOD = "https://api.nasa.gov/planetary/apod"

            if kwargs['startDate'] != None and kwargs['endDate'] != None:
                params = {
                        'api_key':os.environ['API_SECRET_KEY'],
                        'start_date':kwargs['startDate'],
                        'end_date':kwargs['endDate']
                        }
            else:
                params = {
                        'api_key':os.environ['API_SECRET_KEY'],
                        'date':kwargs['date']
                        }
            try:         
                response = requests.get(URL_APOD,params=params)
                # pprint.PrettyPrinter().pprint(response)
                response.raise_for_status()
            
            except requests.RequestException as e:
                self.log.critical('params passed: {}'.format(params))
                self.log.critical(response.text)
                raise ValueError(e)

            # parse json to dictionary
            responseDict = json.loads(response.text)

            # logging returned data
            self.log.info('Information about the image')

            # if date range is passed a list is returned from the api
            if type(responseDict) == list:
                for items in responseDict:
                    for key, value in items.items():
                        self.log.info('{}: {}'.format(key, value.strip()))
                    if items['media_type'].lower() == 'image' and kwargs['saveImage']:
                        downloadedImage = self.downloadPicUrl(kwargs['dir'], items['hdurl'], kwargs['date'])

                        # # open file with default application
                        # self.openImage(downloadedImage)
                    else:
                        self.log.info('Media Type: {} and saveImage value: {} (videos will not be download)'.format(items['media_type'], kwargs['saveImage']))
                        self.openUrl(items['url'])
            else:
                for key, value in responseDict.items():
                    self.log.info('{}: {}'.format(key, value.strip()))

                if responseDict['media_type'].lower() == 'image' and kwargs['saveImage']:
                    downloadedImage = self.downloadPicUrl(kwargs['dir'], responseDict['hdurl'], kwargs['date'])

                    # open file with default application
                    self.openImage(downloadedImage)
                else:
                    self.log.info('Media Type: {} and saveImage value: {} (videos will not be download)'.format(responseDict['media_type'], kwargs['saveImage']))
                    self.openUrl(responseDict['url'])
        except BaseException as e:
            raise ValueError(e)
        
    def __init__(self):        
        self.todayYYYYMMDD = datetime.datetime.now().strftime("%Y-%m-%d")

        self.codePath = os.path.dirname(os.path.realpath(__file__))

        self.log = Logger(os.path.join(self.codePath, 'log', datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.log'))