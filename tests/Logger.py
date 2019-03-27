class Logger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def header(msg):
        print(Logger.HEADER + msg + Logger.ENDC)

    @staticmethod
    def fail(msg):
        print(Logger.FAIL + msg + Logger.ENDC)

    @staticmethod
    def testok(msg):
        print(Logger.OKGREEN + msg + Logger.ENDC)

    @staticmethod
    def stepok(msg):
        print(Logger.OKBLUE + msg + Logger.ENDC)

    @staticmethod
    def info(msg):
        print(msg)

    @staticmethod
    def res(msg):
        print(Logger.WARNING + msg + Logger.ENDC)