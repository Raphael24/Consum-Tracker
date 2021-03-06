#!/usr/bin/python
"""
main.py
Main Logik für den Konsum Tracker
"""

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import dbConsum as db
import time
import log
import os


#init getLogger

consumlogger = log.logger("ConsumLogger", "Main.log")
consumlogger.info("INIT LOGGER MAIN: done")


class ConsumUI(QtWidgets.QDialog):  #class ConsumUI
    def __init__(self, parent=None):
        super().__init__(parent)
        consumlogger.info("MAIN Just for fun")
        self.ui = uic.loadUi('consum.ui', self)
        consumlogger.info("consum.ui load succesfully")
        self.setWindowTitle("Cunsum Tracker")

        print('OK')
        print(db.init_GUI()[0])
        self.i_consum = db.init_GUI()[0]
        self.str_currentDatabase = db.init_GUI()[1]

        self.i_consum_total = db.read_total_consum_of_item(self.str_currentDatabase)
        self.i_consum_total = db.read_total_consum_of_item(self.str_currentDatabase)
        self.i_consum_month = db.read_consum_per_month(self.str_currentDatabase)
        consumlogger.info("INIT: Variablen OK")

        #Init Labels
        self.L_NumbOfConsum.setText(str(self.i_consum)))
        self.L_ConsumToday.setText(str(self.i_consum))
        self.L_ConsumTotal.setText(str(self.i_consum_total))
        self.L_ConsumMonth.setText(str(self.i_consum_month))
        self.L_InsertDBNameFail.setText('Bitte geben Sie einen Namen ein')

        #Init Input
        self.ui.I_DeleteDate.setDate(QDate.currentDate())
        consumlogger.info("INIT: init Labels and Input done")
        print("INIT: init Labels and Input done")


        #Init Combobox
        self.init_ComboBox_Database()
        self.ui.CB_Database.currentIndexChanged.connect(self.changeDatabase)

        # Buttons Datenbank
        self.ui.Btn_Consum.clicked.connect(self.Consum)
        self.ui.Btn_Exit.clicked.connect(self.Exit)
        self.ui.Btn_LoadData.clicked.connect(self.loadData)
        consumlogger.info("INIT: Btn DB done")
        print("INIT: Btn DB done")

        # Buttons Log
        self.ui.Btn_ShowLogMain.clicked.connect(lambda: self.show_log(0))
        self.ui.Btn_ShowLogDB.clicked.connect(lambda: self.show_log(1))
        self.ui.Btn_DeleteMain.clicked.connect(lambda: self.delete_log(0))
        self.ui.Btn_DeleteDB.clicked.connect(lambda: self.delete_log(1))
        self.ui.Btn_ClearLog.clicked.connect(self.clear_log)
        consumlogger.info("INIT: Btn Log done")
        print("INIT: Btn Log done")

        #Buttons Admin
        self.ui.Btn_admin_Insertdata.clicked.connect(db.insert)
        self.ui.Btn_admin_Deletedata.clicked.connect(self.delete)
        self.ui.Btn_admin_Function1.clicked.connect(db.read_consum_Admin)
        self.ui.Btn_Test1.clicked.connect(self.Test1)
        self.ui.Btn_LoadDataAdmin.clicked.connect(self.LoadDataAdmin)
        self.ui.Btn_admin_delFullDatabase.clicked.connect(self.deletFullData)
        consumlogger.info("INIT: Btn Admin done")
        print("INIT: Btn Admin done")

        #Buttons Settings
        self.ui.Btn_CreateDatabase.clicked.connect(self.createDatabase)
        consumlogger.info("INIT: Btn Settings done")
        print("INIT: Btn Settings done")

        #Init Table widget
        Headers = ["Datenbank", "Datum", "Anzahl Konsume"]
        self.TW_Datenbank.setColumnCount(len(Headers))
        self.TW_Datenbank.setRowCount(1)
        self.TW_Datenbank.setHorizontalHeaderLabels(Headers)
        self.loadData()
        consumlogger.info("INIT: table Widget done ")
        print("INIT: table Widget done ")

        #Init Table Widget Admin
        Headers = ["Datenbank", "Datum", "Anzahl Konsume", "Tag"]
        self.TW_DatenbankAdmin.setColumnCount(len(Headers))
        self.TW_DatenbankAdmin.setRowCount(1)
        self.TW_DatenbankAdmin.setHorizontalHeaderLabels(Headers)
        consumlogger.info("INIT: Table Widget Admin")
        self.LoadDataAdmin()
        print("INIT: Table Widget Admin")

        consumlogger.info("INIT: done")


    #---- Combobox -------------------------------------------------------------


    def init_ComboBox_Database(self):
        consumlogger.info("INIT COMBOBOX: Start")
        self.ui.CB_Database.clear()
        self.ui.CB_DeleteData.clear()
        self.ui.CB_DeleteFullData.clear()

        consumlogger.info("INIT COMBOBOX: write items to the CB items: " + str(self.str_currentDatabase))
        self.ui.CB_Database.setCurrentText(str(self.str_currentDatabase))
        consumlogger.info("INIT COMBOBOX: set currentDatabase: " + str(self.str_currentDatabase))
        self.ui.L_title.setText("Consum Tracker - " + str(self.str_currentDatabase))

        data = db.read_items()
        #print('INIT COMBOBOX: ', data)
        if data[0] != '':
            consumlogger.info("INIT COMBOBOX: read items")
            for n in data:
                #print("INIT COMBOBOX: n", n, n[0])
                self.ui.CB_DeleteData.addItem(n[0])
                self.ui.CB_Database.addItem(n[0])
                self.ui.CB_DeleteFullData.addItem(n[0])
        else:
            consumlogger.info("INIT COMBOBOX: No Data avaible")

        consumlogger.info("INIT COMBOBOX: done")


    def changeDatabase(self):
        item = self.ui.CB_Database.currentText()
        self.str_currentDatabase = item

        self.i_consum = db.read_consum_of_item(item)
        self.i_consum_total = db.read_total_consum_of_item(item)
        self.i_consum_month = db.read_consum_per_month(item)

        self.L_NumbOfConsum.setText(str(self.i_consum))
        self.L_ConsumToday.setText(str(self.i_consum))
        self.L_ConsumTotal.setText(str(self.i_consum_total))
        self.L_ConsumMonth.setText(str(self.i_consum_month))

        self.ui.L_title.setText("Consum Tracker - " + item)
        consumlogger.info("Database change: " + item)


    #---- Consum ---------------------------------------------------------------


    def Consum(self): # Consum on the Homepage +1
        if self.str_currentDatabase == '':
            print('CONSUM: No data')
            consumlogger.info("Consumcounter: Keine Daten Vorhanden")
        else:
            self.i_consum += 1
            db.insert_Consum(self.i_consum, self.str_currentDatabase)
            # TODO: eingabe überprüfen str_currentDatabase darf kein leerer string sein

            self.i_consum_total = db.read_total_consum_of_item(self.str_currentDatabase)
            self.i_consum_month = db.read_consum_per_month(self.str_currentDatabase)

            self.L_NumbOfConsum.setText(str(self.i_consum))
            self.L_ConsumToday.setText(str(self.i_consum))
            self.L_ConsumMonth.setText(str(self.i_consum_month))
            self.L_ConsumTotal.setText(str(self.i_consum_total))
            self.loadData()
            self.LoadDataAdmin()
            print(self.str_currentDatabase)
            consumlogger.info("Consumcounter: " + str(self.i_consum))


    #---- Read Data ------------------------------------------------------------


    def loadData(self):
        #print('load data')                                                         #load data for the Homepage
        consumlogger.info("loaddata: Start readconsum: ")
        data = db.read_consum()
        if data == 0:
            consumlogger.info("loaddata: No data avaible(if==0): " + str(data))
            return 0

        AllItems = []

        for kategorie in data:
            for values in kategorie:                                                #read a single item from List [(...),(...),(...)]
                item = values[0]                                                     #read the item on position number 0 (x, y, z)
                numb = str(values[1])                                                #read the item on position number 1 (x, y, z)g
                tag = values[2]
                #print("Item: ", item, "Number:", numb,"Tag: ",tag, "Y:", y )
                #print("TAG", items[2], type(items[2]))
                items = [item, tag, numb]
                AllItems.append(items)

        #print("AllItems", AllItems)
        self.TW_Datenbank.setRowCount(len(AllItems))

        for i in enumerate(AllItems):                                           #a list of all items from one queue
            y = i[0]
            items = i[1]
            for m in range(0,3):                                                # write the items in the table Widget
                Qitem = QtWidgets.QTableWidgetItem(items[m])
                self.TW_Datenbank.setItem(y, m, Qitem)                          #Fill the data in the Table widget

        consumlogger.info("Load data User: Succesfully")


    def LoadDataAdmin(self):
        data = db.read_consum_Admin()
        self.TW_DatenbankAdmin.setRowCount(len(data))                              #calculate the number of rows
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
        consumlogger.info("Load data Admin: Succesfully")


    #---- Write Data -----------------------------------------------------------

    def createDatabase(self):
        name = self.ui.LE_NameDatabase.text()

        #print('Create database: ', name, type(name))
        if name == "" or name == " ":
            self.L_InsertDBNameFail.setText('Bitte einen Namen eingeben')
            consumlogger.info("Creating Database failed: No item selected")
        else:
            print('Create database: Name is Valid', type(name))
            a = db.newDatabase(name)

            if a == False:
                self.L_InsertDBNameFail.setText(str(name) +' ist bereits vorhanden.')
                consumlogger.info("Create database: " + name + " ist bereits vorhanden")
            else:
                self.init_ComboBox_Database()
                self.L_InsertDBNameFail.setText(str(name) +' wurde erfolgreich erstellt')
                self.ui.LE_NameDatabase.setText('')
                consumlogger.info("Create database: " + name )
                print("Create database: OK")

    #---- Delete Data ----------------------------------------------------------

    def delete(self):
        tag = self.ui.I_DeleteDate.date().toPyDate()
        item = self.ui.CB_DeleteData.currentText()
        if item == "":
            consumlogger.info("Deleting database failed: No item selected")
        else:
            db.delete(tag, item)
            consumlogger.info("Deleting of " + item + ": Succesfully")
            self.init_ComboBox_Database()
            self.LoadDataAdmin()

    def deletFullData(self):
        item = self.ui.CB_DeleteFullData.currentText()
        if item == "":
            consumlogger.info("Deleting full data of failed")
        else:
            db.delete_admin(item)
            consumlogger.info("Deleting full data of " + item + ": Succesfully")
            self.init_ComboBox_Database()
            self.LoadDataAdmin()

    #---- Log ------------------------------------------------------------------

    def show_log(self, i):
        self.ui.LW_ListLog.clear()
        Inhalt = log.showlog(i)
        for m in Inhalt:
            self.ui.LW_ListLog.addItem(m)

    def clear_log(self):
        self.ui.LW_ListLog.clear()

    def delete_log(self, i):
        log.deletelog(i)
        self.show_log(i)

    #---- Tests ----------------------------------------------------------------

    def Test1(self):
        consumlogger.info("----- RUN TEST -----")
        self.Consum()
        self.ui.LE_NameDatabase.setText("Testdatabase1")
        self.createDatabase()
        self.ui.CB_Database.setCurrentText("Testdatabase1")
        self.changeDatabase()
        self.Consum()
        self.Consum()
        self.Consum()
        self.ui.CB_DeleteFullData.setCurrentText("Testdatabase1")
        self.deletFullData()
        consumlogger.info("----- END TEST -----")

    def Exit(self):
        self.close()
        consumlogger.info('-------------------- Close Main programm --------------------')


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        dialog = ConsumUI()
        dialog.show()
        consumlogger.info('-------------------- Start Main programm --------------------')
        sys.exit(app.exec())
        print("start")
    except:
        consumlogger.critical("+-+-+-+-+-+-+-+-+-+-+-+ GUI Closed +-+-+-+-+-+-+-+-+-+-+-+")
