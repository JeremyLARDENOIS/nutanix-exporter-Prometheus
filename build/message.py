from datetime import datetime

_OK = '\033[92m' #GREEN
_WARNING = '\033[93m' #YELLOW
_FAIL = '\033[91m' #RED
_RESET = '\033[0m' #RESET COLOR 

def ok(msg):
    print(f"{_OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] {msg}{_RESET}")
def warning(msg):
    print(f"{_WARNING}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [WARNING] {msg}{_RESET}")
def error(msg):
    print(f"{_FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {msg}{_RESET}")