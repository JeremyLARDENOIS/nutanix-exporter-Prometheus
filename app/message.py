from datetime import datetime

_SUCCESS = '\033[92m' #GREEN
_INFO = '\033[34m' # BLUE
_WARNING = '\033[93m' #YELLOW
_FAIL = '\033[91m' #RED
_RESET = '\033[0m' #RESET COLOR 

def success(msg):
    print(f"{_SUCCESS}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [SUCCESS] {msg}{_RESET}")
def info(msg):
    print(f"{_INFO}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] {msg}{_RESET}")
def warning(msg):
    print(f"{_WARNING}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [WARNING] {msg}{_RESET}")
def error(msg):
    print(f"{_FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {msg}{_RESET}")