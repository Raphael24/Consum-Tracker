import time
import datetime

now = datetime.datetime.now()
today = datetime.datetime.today()
timeact = time.time()
#print(timeact,", ", type(now), today, ", ", type(today))


now = time.localtime(time.time())                                       #convert UNIX time in struct_time
#print("2")
now = time.strftime("%Y-%m-%d %H:%M:%S", now)
print(now, type(now))
#cur.execute("SELECT datum as 'datum[date]' FROM consum")
data = [('2021-09-23 10:42:37',), ('2021-09-23 10:42:38',), ('2021-09-23 10:44:04',), ('2021-09-23 10:44:07',), ('2021-09-23 10:44:31',), ('2021-09-23 10:44:32',), ('2021-09-23 10:46:03',)]
#data = ('2021-09-23 10:42:37',)
#print("Zeit:", data, type(data))

for n in data:
    #print("n from Data",n, type(n))
    for m in n:
        #print("n from Data in string",m, type(n))
        m = str(m)
        #print("n from Data in string",m, type(n))
        timee = time.strptime(m, "%Y-%m-%d %H:%M:%S")
        #print("---------Time korrekt ----------", timee)



"""
now = datetime.datetime.now()
today = datetime.datetime.today()

cur.execute("INSERT INTO testdate(datum, timestamp) VALUES (?, ?)", (today, now))
cur.execute("SELECT datum, timestamp FROM testdate")
row = cur.fetchone()
print(row)                                                        #Fetchone gibt die Datensätze als Tupel zurück
print("Datum: ",today, "=>", row[0], type(row[0]))
print("Zeit: ", now, "=>", row[1], type(row[1]))
print()


cur.execute("SELECT current_date as 'Datum [date]', current_timestamp as 'timestamp[timestamp]'")
row = cur.fetchone()
print("current_date: ", row[0], type(row[0]))
print("current_timestamp: ", row[1], type(row[1]))
"""
