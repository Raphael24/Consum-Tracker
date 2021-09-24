#!/usr/bin/python

"""
Dies ist ein Docstring von Consumtracker
"""

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import dbConsum as db
import time
import logging

logging.basicConfig(filename = "consum.log",
                    level = logging.INFO,
                    style = "{",
                    format = "{asctime}{levelname:8}{message}",
                    datefmt = "%Y-%m-%d %H:%M:%S")



class ConsumUI(QtWidgets.QDialog):  #class ConsumUI
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi(r'D:\Projekt1\KonsumProgramm\consum.ui', self)
        self.setWindowTitle("Cunsum Tracker")
        self.i_consum = db.init_GUI()
        self.str_currentDatabase = 'Huere Michi'

        #Init Labels
        self.L_NumbOfConsum.setText(str(self.i_consum))
        self.L_ConsumToday.setText(str(self.i_consum))
        self.L_ConsumTotal.setText(str(self.i_consum))


        #Init Input
        self.ui.I_DeleteDate.setDate(QDate.currentDate())


        #Init Combobox
        self.init_ComboBox_Database()
        self.ui.CB_Database.currentIndexChanged.connect(self.changeDatabase)


        #Connect Buttons
        self.ui.Btn_Consum.clicked.connect(self.Consum)
        self.ui.Btn_Exit.clicked.connect(self.Exit)
        self.ui.Btn_LoadData.clicked.connect(self.loadData)
        #Buttons Admin
        self.ui.Btn_admin_Insertdata.clicked.connect(db.insert)
        self.ui.Btn_admin_Deletedata.clicked.connect(self.delete)
        self.ui.Btn_admin_Function1.clicked.connect(db.read_consum_Admin)
        self.ui.Btn_admin_Function2.clicked.connect(db.read_consum)
        self.ui.Btn_LoadDataAdmin.clicked.connect(self.LoadDataAdmin)
        self.ui.Btn_admin_delFullDatabase.clicked.connect(self.deletFullData)
        #Buttons Settings
        self.ui.Btn_CreateDatabase.clicked.connect(self.createDatabase)

        #Init Table widget
        Headers = ["Datenbank", "Datum", "Anzahl Konsume"]
        self.TW_Datenbank.setColumnCount(len(Headers))
        self.TW_Datenbank.setRowCount(1)
        self.TW_Datenbank.setHorizontalHeaderLabels(Headers)
        self.loadData()

        #Init Table Widget Admin
        Headers = ["Datenbank", "Datum", "Anzahl Konsume", "Tag"]
        self.TW_DatenbankAdmin.setColumnCount(len(Headers))
        self.TW_DatenbankAdmin.setRowCount(1)
        self.TW_DatenbankAdmin.setHorizontalHeaderLabels(Headers)
        self.LoadDataAdmin()

        print("INIT DONE")

    def fake(self):
        pass


    #---- Combobox -------------------------------------------------------------


    def init_ComboBox_Database(self):
        print("init start Combobox")
        self.ui.CB_Database.clear()
        self.ui.CB_DeleteData.clear()
        self.ui.CB_DeleteFullData.clear()
        data = db.read_items()
        for n in data:
            self.ui.CB_DeleteData.addItem(n[0])
            self.ui.CB_Database.addItem(n[0])
            self.ui.CB_DeleteFullData.addItem(n[0])

    def changeDatabase(self):
        item = self.ui.CB_Database.currentText()
        self.str_currentDatabase = item
        NumbOfConsum = db.read_consum_of_item(item)
        self.L_NumbOfConsum.setText(str(NumbOfConsum))
        self.L_ConsumToday.setText(str(NumbOfConsum))
        self.L_ConsumTotal.setText(str(NumbOfConsum))
        self.i_consum = NumbOfConsum
        print("Fuck")
        self.ui.L_title.setText("Consum Tracker - " + item)


    #---- Consum ---------------------------------------------------------------


    def Consum(self): # Consum on the Homepage +1
        #print("StartConsum")
        self.i_consum += 1
        #print("Consume: ", self.i_consum)
        self.L_NumbOfConsum.setText(str(self.i_consum))
        self.L_ConsumToday.setText(str(self.i_consum))
        print(self.str_currentDatabase)
        db.insert_Consum(self.i_consum, self.str_currentDatabase)

        logging.log(logging.INFO, "Consumcounter: +1")
        #time.sleep(5)


    #---- Read Data ------------------------------------------------------------


    def loadData(self):                                                         #load data for the Homepage
        data = db.read_consum()
        self.TW_Datenbank.setRowCount(len(data))                                #calculate the number of rows
        for n in range(0, len(data)):                                           #Fill the data in the Table widget
            y = n
            items = data[n]                                                     #read a single item from List [(...),(...),(...)]
            item = items[0]                                                     #read the item on position number 0 (x, y, z)
            numb = str(items[1])                                                #read the item on position number 1 (x, y, z)g
            tag = items[2]
            #print("Item: ",item, "Number:",numb,"Tag: ",tag)            #log Message
            #print("TAG", items[2], type(items[2]))
            items = [item, tag, numb]                                            #a list of all items from one queue
            for m in range(0,3):                                                # write the items in the table Widget
                Qitem = QtWidgets.QTableWidgetItem(items[m])
                self.TW_Datenbank.setItem(y, m, Qitem)


    def LoadDataAdmin(self):
        print("loadData Admin")
        data = db.read_consum_Admin()
        self.TW_DatenbankAdmin.setRowCount(len(data))                              #calculate the number of rows
        #print("Check 1")
        for n in range(0, len(data)):                                           #Fill the data in the Table widget
            y = n
            items = data[n]                                                     #read a single item from List [(...),(...),(...)]
            item = items[0]                                                     #read the item on position number 0 (x, y, z)
            numb = str(items[1])                                                #read the item on position number 1 (x, y, z)
            timestamp = items[2]
            tag = items[3]
            #print("Item: ",item, "Number:",numb,"Time: ",timestamp)             #log Message
            #print("TAG", items[3], type(items[3]))
            items = [item, timestamp, numb, tag]                                     #a list of all items from one queue
            for m in range(0,4):                                                # write the items in the table Widget
                Qitem = QtWidgets.QTableWidgetItem(items[m])
                self.TW_DatenbankAdmin.setItem(y, m, Qitem)


    #---- Write Data -----------------------------------------------------------
    def createDatabase(self):
        name = self.ui.LE_NameDatabase.text()
        db.newDatabase(name)
        self.init_ComboBox_Database()




    #---- Delete Data ----------------------------------------------------------
    def delete(self):
        print("delete")
        tag = self.ui.I_DeleteDate.date().toPyDate()
        item = self.ui.CB_DeleteData.currentText()
        if item == "":
            print("fail")
            print("item",item, type(item))
        else:
            db.delete(tag, item)
            self.init_ComboBox_Database()
            self.LoadDataAdmin()

    def deletFullData(self):
        print("delete FUll Data")
        item = self.ui.CB_DeleteFullData.currentText()
        if item == "":
            print("fail")
            print("item",item, type(item))
        else:
            db.delete_admin(item)
            self.init_ComboBox_Database()
            self.LoadDataAdmin()


    def Exit(self):
        self.close()



app = QtWidgets.QApplication(sys.argv)
dialog = ConsumUI()
dialog.show()
sys.exit(app.exec())
print("start")

logging.log(logging.CRITICAL, "GUI not start")
