# Defines logfile
import logging

log_files = ["Main.log", "Database.log"]

def showlog(i):
    logfile = open(log_files[i], "r")
    Inhalt = logfile.readlines()
    logfile.close()
    return Inhalt

def deletelog(i):
    logfile = open(log_files[i], "w")
    logfile.truncate()
    logfile.close()

def logger(name, file):
    name, file = str(name), str(file)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(file)
    fh.setLevel(logging.INFO)
    frm = logging.Formatter("{asctime} {levelname:8} {message}", "%Y.%m.%d %H:%M:%S", style="{")
    fh.setFormatter(frm)
    logger.addHandler(fh)
    return logger
