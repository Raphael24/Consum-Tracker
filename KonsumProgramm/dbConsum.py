import sqlite3
import datetime
import time
import random
import log

#configuration Logging
consumlogger = log.logger("ConsumLoggerDB", "Database.log")
consumlogger.info("INIT LOGGER DB: done")

consumlogger.info('-------------------- Start Database programm --------------------')

#Database connection
consumlogger.info('-------------------- Just for Fun --------------------')
connection = sqlite3.connect("consum.db")
consumlogger.info('--------------------DB load succesfully --------------------')
cur = connection.cursor()

#Database Structure
cur.execute("""CREATE TABLE IF NOT EXISTS consum (
                    item TEXT,
                    NumbOfConsum INTEGER,
                    datum TIMESTAMP,
                    tag TIMESTAMP
            )""")

cur.execute("""CREATE TABLE IF NOT EXISTS consumperday (
                    item TEXT,
                    day TIME,
                    NumbOfConsum INTEGER
            )""")

#-----------------------All Actions from writing the Database-------------------

def insert_Consum(NumbOfConsum, item="Huere Michi"):
    try:
        now = time.localtime(time.time())                                       #convert UNIX time in struct_time
        tag = time.strftime("%Y-%m-%d", now)
        now = time.strftime("%Y-%m-%d %H:%M:%S", now)
        #tag = '2021-09-16'
        #print("Time OK: ", now, tag)
        cur.execute("SELECT tag FROM consum WHERE tag=:tag AND item=:item", {"tag" : tag, "item" : item})
        data = cur.fetchone()
        #print("Zeit:", data, type(data))
        if data is None:
            #print("Es wurde kein Passender Datensatz gefunden:", item, NumbOfConsum, now, tag)
            cur.execute("INSERT INTO consum(item, NumbOfConsum, datum, tag) VALUES (?, ?, ?, ?)", (item, NumbOfConsum, now, tag))
            #print("commit")
            connection.commit()
            consumlogger.info("Datensatz: " + item + " wurde erfolgreich erstellt")
            #print("Succesfully INSERT: ", NumbOfConsum, item)
        else:
            print("Es wurde ein Passender Datensatz gefunden")
            #print("Datenüberprüfen:", NumbOfConsum, type(NumbOfConsum), tag,type(tag), item,type(item))
            cur.execute("UPDATE consum SET NumbOfConsum=:value1 WHERE tag=:tag AND item=:item", {"value1" : NumbOfConsum, "tag" : tag, "item" : item})
            connection.commit()
            print("Succesfully UPDATE: ", NumbOfConsum, item)
            consumlogger.info("Datensatz: " + item + " wurde erfolgreich Aktualisiert: " + str(NumbOfConsum))

    except:
        #print("INSERT_COMSUM: Ein Problem trat auf -> Rollback")
        connection.rollback()
        consumlogger.Error("INSERT_COMSUM: Ein Problem trat(" + item + ") auf -> Rollback")


def insert(): #only for Admins
    try:
        now = time.localtime(time.time())                                       #convert UNIX time in struct_time
        now = time.strftime("%Y-%m-%d %H:%M:%S", now)
        tag = time.strftime("%Y-%m-%d", now)
        tag = '2021-09-10'
        #print("INSERT:",now)
        item = "Huere Michi"
        for i in range(1,2):
            NumbOfConsum = (random.randint(1,10))
            cur.execute("INSERT INTO consum(item, NumbOfConsum, datum, tag) VALUES (?, ?, ?, ?)", (item, NumbOfConsum, now, tag))
            connection.commit()
            #print("Succesfully Insert TEST: ", NumbOfConsum)
            consumlogger.info("TEST INSERT: Datensatz wurde erfolgreich erstellt.")
    except:
        #print("INSERT: Ein Problem trat auf -> Rollback")
        connection.rollback()
        consumlogger.info("TEST INSERT: Ein Problem trat auf -> Rollback")

def newDatabase(item):
    try:
        now = time.localtime(time.time())                                       #convert UNIX time in struct_time
        tag = time.strftime("%Y-%m-%d", now)
        now = time.strftime("%Y-%m-%d %H:%M:%S", now)
        cur.execute("SELECT item FROM consum WHERE item=:item", {"item" : item})
        #print("Zeit:", data[0], type(data[0]))
        data = cur.fetchone()

        if data is None:
            #print("Es wird ein neuer Eintrag erstellt")
            cur.execute("INSERT INTO consum(item, NumbOfConsum, datum, tag) values(?, ?, ?, ?)", (item, 0, now, tag))
            connection.commit()
            #print("Succesfully Insert Database: ", item)
            consumlogger.info("INSERT NEW DATABASE: " + item)
        else:
            #print("Datensatz bereits Vorhanden")
            consumlogger.info("INSERT NEW DATABASE: " + item + " ist bereits vorhanden")
    except:
        consumlogger.error("INSERT NEW DATABASE: Ein Problem trat auf -> Rollback")
        #print("INSERT NEW DATABASE: Ein Problem trat auf -> Rollback")
        connection.rollback()


#-----------------------All Actions from reading the Database-------------------

def read_consum_Admin():
    cur.execute("SELECT item, NumbOfConsum, datum, tag FROM consum ORDER BY item ASC ")
    data = cur.fetchall()
    return data

def read_consum():
    cur.execute("SELECT item, MAX(NumbOfConsum), tag  FROM consum GROUP BY item ORDER BY item ASC")
    data = cur.fetchall()
    return data

def read_consum_of_item(item):
    now = time.localtime(time.time())                                       #convert UNIX time in struct_time
    tag = time.strftime("%Y-%m-%d", now)
    cur.execute("SELECT NumbOfConsum FROM consum WHERE item=:item AND tag=:tag", {"item" : item, "tag" : tag})
    data = cur.fetchone()
    if data is None:
        return 0
    else:
        return data[0]

def Consum_total():
    try:
        cur.execute("SELECT MAX(NumbOfConsum) FROM consum")
        data = cur.fetchone()
        return data[0]
    except:
        return 0


def Comsum_Month():
    # TODO:
    pass

def read_items():
    cur.execute("SELECT item from consum GROUP BY item")
    data = cur.fetchall()
    return data

#-----------------------All Actions from deleting the Database------------------

def delete(tag, item):
    try:
        cur.execute("DELETE FROM consum WHERE tag=:tag AND item=:item", {"tag": tag, "item" : item})
        connection.commit()
        data = cur.fetchone()
        consumlogger.info("DELETE DATABASE: " + item + " Succesfully")
        return data[0]
    except:
        connection.rollback()
        consumlogger.error("DELETE DATABASE: Ein Problem trat auf -> Rollback")
        return 0


def delete_admin(item):
    try:
        cur.execute("DELETE FROM consum WHERE item=:item", {"item" : item})
        connection.commit()
        data = cur.fetchone()
        consumlogger.info("DELETE FULL DATABASE: " + item + " Succesfully")
    except:
        connection.rollback()
        consumlogger.error("DELETE FULL DATABASE: Ein Problem trat auf -> Rollback")
        return 0



def init_GUI():
    now = time.localtime(time.time())                                       #convert UNIX time in struct_time
    tag = time.strftime("%Y-%m-%d", now)
    try:
        cur.execute("SELECT MAX(NumbOfConsum) FROM consum WHERE tag=:tag", {"tag": tag })
        data = cur.fetchone()

        if data[0] == None:
            #print("No data avaible:")
            return 0
        else:
            #print("Data avaivle", data[0])
            return data[0]
    except:
        consumlogger.error("INIT GUI: FAIL (Database not Load) ")
        return 0





#init_GUI()
#insert()
#insert_Consum(5)
