class Logger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    test = ""
    verbosity = False

    @classmethod
    def set_test(cls, nb):
        if nb == "":
            cls.test = "---"
        else:
            cls.test = f"[Test {nb}]"

    @classmethod
    def set_verbosity(cls, v):
        cls.verbosity = v

    @classmethod
    def header(cls, msg):
        print(f"{Logger.HEADER}{cls.test} {msg}{Logger.ENDC}")

    @classmethod
    def fail(cls, msg):
        print(f"{Logger.FAIL}{cls.test} {msg}{Logger.ENDC}")

    @classmethod
    def testok(cls, msg):
        print(f"{Logger.OKGREEN}{cls.test} {msg}{Logger.ENDC}")

    @classmethod
    def stepok(cls, msg):
        if cls.verbosity:
            print(f"{Logger.OKBLUE}{cls.test} {msg}{Logger.ENDC}")

    @classmethod
    def info(cls, msg):
        if cls.verbosity:
            print(f"{Logger.ENDC}{cls.test} {msg}{Logger.ENDC}")

    @classmethod
    def res(cls, msg):
        print(f"{Logger.WARNING}{cls.test} {msg}{Logger.ENDC}")
