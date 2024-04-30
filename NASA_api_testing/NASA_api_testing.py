import traceback, os, getopt, sys

from APIs import NASA_APIs

try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['date='])
    optsDict = {}
    optsDict.update(dict(opts))

    apiCall = NASA_APIs() 

    if '--date' in optsDict:
        _tempDate = optsDict['--date']
        date = apiCall.try_parsing_date(_tempDate)
    else:
        date = apiCall.todayYYYYMMDD 
        
    '''
    APOD
    
    One of the most popular websites at NASA is the Astronomy Picture of the Day. In fact, this website is one of the most popular websites across all federal agencies. 
    It has the popular appeal of a Justin Bieber video. This endpoint structures the APOD imagery and associated metadata so that it can be repurposed for other applications.
    In addition, if the concept_tags parameter is set to True, then keywords derived from the image explanation are returned. These keywords could be used as auto-generated 
    hashtags for twitter or instagram feeds; but generally help with discoverability of relevant imagery.

    The full documentation for this API can be found in the APOD API Github repository.
    ''' 
                     
    apiCall.fetchAPOD(date, saveImage=True, dir=os.path.join(os.getcwd(), 'APOD_Images'))

    apiCall.log.info('Process Complete')

    apiCall.log.closeLogger()
except:
    apiCall.log.critical(traceback.print_exc())
    apiCall.log.closeLogger()    
    
    