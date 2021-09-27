# Defines logfile
log_files = ["KonsumProgramm\Main.log", "KonsumProgramm\Database.log"]

def showlog(i):
    logfile = open(log_files[i], "r")
    Inhalt = logfile.readlines()
    logfile.close()
    return Inhalt

def deletelog(i):
    logfile = open(log_files[i], "w")
    logfile.truncate()
    logfile.close()
