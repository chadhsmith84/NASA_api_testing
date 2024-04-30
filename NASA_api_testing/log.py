import os, logging, datetime, traceback

class Logger(object):
    def __createLogDirectory(self, logDirectory):

        logDirectory = os.path.join(logDirectory)

        if not os.path.exists(logDirectory):
            os.makedirs(logDirectory)
            print('directory {} created'.format(logDirectory))

        return logDirectory

    def __defineLog(self, logDirectory, logFile):
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-2s %(levelname)-2s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=os.path.join(logDirectory, logFile),
                            filemode='a')

        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        # set a format which is simpler for console use
        formatter = logging.Formatter('%(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

        logging.info('Process Started: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")))

    def info(self, msg):
        logging.info(msg)

    def critical(self, msg):
        logging.critical(msg)

    def error(self, msg):
        logging.error(msg)

    def closeLogger(self):
        logging.shutdown()

    # #logFile = file path with full file name
    #def __init__(self, directory, logFileName):
    #    self.logDirectory = directory
    #    self.logFile = logFileName

    #    # check if log directory exist
    #    self.__createLogDirectory(logDirectory)

    #    # set up logger
    #    self.log = self.__defineLog(self.logDirectory, self.logFile)

    def __init__(self, logFileNameWithPath):

        # checking if path was provided
        if not os.path.dirname(logFileNameWithPath):
            raise ValueError('file {} does not contain a full path.'.format(logFileNameWithPath))

        self.logDirectory = os.path.split(logFileNameWithPath)[0]
        self.logFile = os.path.split(logFileNameWithPath)[-1]

        try:
            # check if log directory exist
            self.logDirectory = self.__createLogDirectory(self.logDirectory)

            # set up logger
            self.__defineLog(self.logDirectory, self.logFile)
        except:
            traceback.print_exc() 