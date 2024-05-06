import traceback, os, getopt, sys

from APIs import NASA_APIs

try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['project=', 'date=', 'startDate=', 'endDate='])
    optsDict = {}
    optsDict.update(dict(opts))

    apiCall = NASA_APIs()

    if '--project' in optsDict:
        _project = optsDict['--project']
        if _project.lower() == 'apod':
            if '--date' in optsDict and '--startDate' in optsDict and '--endDate' in optsDict:
                raise ValueError('must provide --date OR --startDate and --endDate. Both cannot be provided')
            else:
                if '--date' in optsDict:
                    _tempDate = optsDict['--date']
                    date = apiCall.try_parsing_date(_tempDate)
                else:
                    date = apiCall.todayYYYYMMDD 
                if '--startDate' in optsDict:
                    _tempStartDate = optsDict['--startDate']
                    startDate = apiCall.try_parsing_date(_tempStartDate)
                else:
                    startDate = None
                if '--endDate' in optsDict:
                    _tempEndDate = optsDict['--endDate']
                    endDate = apiCall.try_parsing_date(_tempEndDate)
                else:
                    endDate = None


    '''
    APOD
    
    One of the most popular websites at NASA is the Astronomy Picture of the Day. In fact, this website is one of the most popular websites across all federal agencies. 
    It has the popular appeal of a Justin Bieber video. This endpoint structures the APOD imagery and associated metadata so that it can be repurposed for other applications.
    In addition, if the concept_tags parameter is set to True, then keywords derived from the image explanation are returned. These keywords could be used as auto-generated 
    hashtags for twitter or instagram feeds; but generally help with discoverability of relevant imagery.

    The full documentation for this API can be found in the APOD API Github repository.
    ''' 
    try:
        if _project.lower() == 'apod':
            apiCall.fetchAPOD(date=date, startDate=startDate, endDate=endDate, saveImage=False, dir=os.path.join(apiCall.codePath, 'APOD_Images'))
    

        apiCall.log.info('Process Complete')
    except BaseException as e:
        apiCall.log.critical(e)
        apiCall.log.closeLogger()
except BaseException as e:
    traceback.print_exc()
