import sqlite3
import datetime
import time
import random
import log

# ----------configuration Logging ----------

consumlogger = log.logger("ConsumLoggerDB", "Database.log")
consumlogger.info("INIT LOGGER DB: done")
consumlogger.info('-------------------- Start Database programm --------------------')

# ----------Database connection ----------

consumlogger.info('-------------------- Just for Fun --------------------')
connection = sqlite3.connect("consum.db")
consumlogger.info('--------------------DB load succesfully --------------------')
cur = connection.cursor()

#---------- Globale variablen ----------

akt_zeit = time.localtime(time.time())      #convert UNIX time in struct_time
akt_monat = time.strftime("%m", akt_zeit)
akt_tag = time.strftime("%Y-%m-%d", akt_zeit)
akt_zeit_form = time.strftime("%Y-%m-%d %H:%M:%S", akt_zeit)

# ----------Database Structure ----------

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
        cur.execute("SELECT tag FROM consum WHERE tag=:tag AND item=:item", {"tag" : akt_tag, "item" : item})
        data = cur.fetchone()

        if data is None:
            #print("Es wurde kein Passender Datensatz gefunden:", item, NumbOfConsum, now, tag)
            cur.execute("INSERT INTO consum(item, NumbOfConsum, datum, tag) VALUES (?, ?, ?, ?)", (item, NumbOfConsum, akt_zeit_form, akt_tag))
            #print("commit")
            connection.commit()
            consumlogger.info("Datensatz: " + item + " wurde erfolgreich erstellt")
            #print("Succesfully INSERT: ", NumbOfConsum, item)
        else:
            print("Es wurde ein Passender Datensatz gefunden")
            #print("Datenüberprüfen:", NumbOfConsum, type(NumbOfConsum), tag,type(tag), item,type(item))
            cur.execute("UPDATE consum SET NumbOfConsum=:value1 WHERE tag=:tag AND item=:item", {"value1" : NumbOfConsum, "tag" : akt_tag, "item" : item})
            connection.commit()
            print("Succesfully UPDATE: ", NumbOfConsum, item)
            consumlogger.info("Datensatz: " + item + " wurde erfolgreich Aktualisiert: " + str(NumbOfConsum))

    except:
        #print("INSERT_COMSUM: Ein Problem trat auf -> Rollback")
        connection.rollback()
        consumlogger.Error("INSERT_COMSUM: Ein Problem trat(" + item + ") auf -> Rollback")


def insert(): #only for Admins
    print('DB ok insert')
    try:
        print('DB try OK')
        item = "Huere Michi"
        print('Check 4')
        for i in range(1,2):
            NumbOfConsum = (random.randint(1,10))
            cur.execute("INSERT INTO consum(item, NumbOfConsum, datum, tag) VALUES (?, ?, ?, ?)", (item, NumbOfConsum, akt_zeit_form, akt_tag))
            connection.commit()
            #print("Succesfully Insert TEST: ", NumbOfConsum)
            consumlogger.info("TEST INSERT: Datensatz wurde erfolgreich erstellt.")
    except:
        #print("INSERT: Ein Problem trat auf -> Rollback")
        connection.rollback()
        consumlogger.info("TEST INSERT: Ein Problem trat auf -> Rollback")


def newDatabase(item):
    try:
        cur.execute("SELECT item FROM consum WHERE item=:item", {"item" : item})
        #print("Zeit:", data[0], type(data[0]))
        data = cur.fetchone()

        if data is None:
            #print("Es wird ein neuer Eintrag erstellt")
            cur.execute("INSERT INTO consum(item, NumbOfConsum, datum, tag) values(?, ?, ?, ?)", (item, 0, akt_zeit_form, akt_tag))
            connection.commit()
            #print("Succesfully Insert Database: ", item)
            consumlogger.info("INSERT NEW DATABASE: " + item)
        else:
            #print("Datensatz bereits Vorhanden")
            consumlogger.info("INSERT NEW DATABASE: " + item + " ist bereits vorhanden")
            return False
    except:
        consumlogger.error("INSERT NEW DATABASE: Ein Problem trat auf -> Rollback")
        #print("INSERT NEW DATABASE: Ein Problem trat auf -> Rollback")
        connection.rollback()


#-----------------------All Actions from reading the Database-------------------

def read_items():
    cur.execute("SELECT item FROM consum GROUP BY item")
    data = cur.fetchall()
    print('read_items: ', data)
    if len(data) == 0:
        consumlogger.info("READ ITEMS: No data")
        data.insert(0, '')
        return data
    else:
        consumlogger.info("READ ITEMS: Succesfulls")
        return data


def read_consum_Admin():
    cur.execute("SELECT item, NumbOfConsum, datum, tag FROM consum ORDER BY item ASC ")
    data = cur.fetchall()

    print('read_consum_Admin', data)
    if data is None:
        return []

    return data


def read_consum():
    consums = []
    items = read_items()
    len_items = len(items)
    item = items[0]

    if item == '':
        return consums
    else:
        for i in range(0, len_items):                                               #durchläuft die verschiedenen Kategorien und sucht den maximalwert der Spalte "NumbOfConsum"
            item = items[i]
            item = item[0]
            cur.execute("SELECT item, MAX(NumbOfConsum), tag FROM consum WHERE item=:item GROUP BY tag", {"item" : item})
            data = cur.fetchall()
            consums.append(data)
        return consums                                                          #eine liste in der jede Kategorie genau einmal enthält


def read_test():
    cur.execute("SELECT item FROM consum GROUP BY item ORDER BY item ASC")
    data = cur.fetchall()
    print(data)
    return data


def read_consum_of_item(item):
    cur.execute("SELECT NumbOfConsum FROM consum WHERE item=:item AND tag=:tag", {"item" : item, "tag" : akt_tag})
    data = cur.fetchone()

    if data is None:
        return 0
    else:
        return data[0]

def read_total_consum_of_item(item):
    cur.execute("SELECT SUM(NumbOfConsum) FROM consum WHERE item=:item", {"item" : item})
    data = cur.fetchone()
    if data[0] is None:
        return 0
    else:
        return data[0]

def read_consum_per_month(item):
    cur.execute("SELECT SUM(NumbOfConsum) FROM consum WHERE strftime('%m', tag) =:month AND item=:item", {"item" : item, "month" : akt_monat})
    data = cur.fetchone()
    if data[0] is None:
        return 0
    else:
        return data[0]

#a = read_consum_per_month('furz')
#print(a)
#comsum_Month('Kaffi')

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
#delete_admin('')

def init_GUI():
    initlist = []
    try:
        cur.execute("SELECT MAX(NumbOfConsum) FROM consum WHERE tag=:tag ", {"tag": akt_tag })
        data = cur.fetchone()

        cur.execute("SELECT item FROM consum ")
        item = cur.fetchone()
        #print("Item: ", item, type(item))
        initlist.append(data[0])
        initlist.append(item)

        if item is None:
            #print('Type = None')
            initlist[1] = ''

        if isinstance(item, tuple):
            #print('Type = tupel')
            if item[0] == '':
                #print('Tupel: no data')
                initlist[1] = ''
            else:
                #print('Tupel: has data')
                initlist[1] = item[0]

        if data[0] == None:
            initlist[0] = 0
            return initlist

        else:
            return initlistt

    except:
        consumlogger.error("INIT GUI: FAIL (Database not Load) ")
        a = [0, '']
        return a


#a = init_GUI()
#print(a)
#insert()
#insert_Consum(5)
