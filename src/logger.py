from enum import Enum
from colorama import Fore, Back, Style
import os
from datetime import date, datetime

class LogSeverity(str, Enum):
    DEBUG = Fore.WHITE
    LOG = Fore.CYAN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    FATAL = Fore.BLACK + Back.RED

def _create_log_directory() -> None:
    if not os.path.isdir("LOGDUMP"):
        os.makedirs("LOGDUMP")

def _dump_log(severity:LogSeverity, title:str, message:str) -> None:
    try:
        _create_log_directory()
        fileName = "LOGDUMP/LOG_" + str(date.today()) + ".log"
        logFile = open(fileName, "a")
        # (TIMESTAMP) [SEVERITY] TITLE :: MESSAGE
        logFile.write("(" + str(datetime.now()) + ") [" + severity.name + "] " + title + " :: " + message + "\r\n")
        logFile.close()
    except Exception as e:
        log(LogSeverity.ERROR, "Failed to Dump Log", str(e), False)

def log(severity:LogSeverity, title:str, message:str, dumpLog = True) -> None:
    # [SEVERITY] TITLE :: MESSAGE 
    print(severity + "[" + severity.name  + "] " + title + " :: " + message + Style.RESET_ALL)
    if dumpLog:
        _dump_log(severity, title, message)
