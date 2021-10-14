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

        self.i_consum = db.init_GUI()[0]
        self.str_currentDatabase = db.init_GUI()[1]
        self.i_consum_total = db.read_total_consum_of_item(self.str_currentDatabase)
        self.i_consum_total = db.read_total_consum_of_item(self.str_currentDatabase)
        self.i_consum_month = db.read_consum_per_month(self.str_currentDatabase)

        #Init Labels
        self.L_NumbOfConsum.setText(str(self.i_consum))
        self.L_ConsumToday.setText(str(self.i_consum))
        self.L_ConsumTotal.setText(str(self.i_consum_total))
        self.L_ConsumMonth.setText(str(self.i_consum_month))

        #Init Input
        self.ui.I_DeleteDate.setDate(QDate.currentDate())

        #Init Combobox
        self.init_ComboBox_Database()
        self.ui.CB_Database.currentIndexChanged.connect(self.changeDatabase)

        # Buttons Datenbank
        self.ui.Btn_Consum.clicked.connect(self.Consum)
        self.ui.Btn_Exit.clicked.connect(self.Exit)
        self.ui.Btn_LoadData.clicked.connect(self.loadData)

        # Buttons Log
        self.ui.Btn_ShowLogMain.clicked.connect(lambda: self.show_log(0))
        self.ui.Btn_ShowLogDB.clicked.connect(lambda: self.show_log(1))
        self.ui.Btn_DeleteMain.clicked.connect(lambda: self.delete_log(0))
        self.ui.Btn_DeleteDB.clicked.connect(lambda: self.delete_log(1))
        self.ui.Btn_ClearLog.clicked.connect(self.clear_log)

        #Buttons Admin
        self.ui.Btn_admin_Insertdata.clicked.connect(db.insert)
        self.ui.Btn_admin_Deletedata.clicked.connect(self.delete)
        self.ui.Btn_admin_Function1.clicked.connect(db.read_consum_Admin)
        self.ui.Btn_Test1.clicked.connect(self.Test1)
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

        consumlogger.info("INIT: done")

    def fake(self):
        pass


    #---- Combobox -------------------------------------------------------------


    def init_ComboBox_Database(self):
        self.ui.CB_Database.clear()
        self.ui.CB_DeleteData.clear()
        self.ui.CB_DeleteFullData.clear()
        data = db.read_items()
        for n in data:
            self.ui.CB_DeleteData.addItem(n[0])
            self.ui.CB_Database.addItem(n[0])
            self.ui.CB_DeleteFullData.addItem(n[0])
        consumlogger.info("INIT COMBOBOX: done")
        self.ui.CB_Database.setCurrentText(self.str_currentDatabase)
        self.ui.L_title.setText("Consum Tracker - " + self.str_currentDatabase)

    def changeDatabase(self):
        item = self.ui.CB_Database.currentText()
        self.str_currentDatabase = item

        NumbOfConsum = db.read_consum_of_item(item)
        TotalConsum = db.read_total_consum_of_item(item)
        TotalConsum_month = db.read_consum_per_month(item)

        self.L_NumbOfConsum.setText(str(NumbOfConsum))
        self.L_ConsumToday.setText(str(NumbOfConsum))
        self.L_ConsumTotal.setText(str(TotalConsum))
        self.i_consum = NumbOfConsum
        self.i_consum_total = TotalConsum
        self.i_consum_month = TotalConsum_month
        self.ui.L_title.setText("Consum Tracker - " + item)
        consumlogger.info("Database change: " + item)


    #---- Consum ---------------------------------------------------------------


    def Consum(self): # Consum on the Homepage +1
        self.i_consum += 1
        self.L_NumbOfConsum.setText(str(self.i_consum))
        self.L_ConsumToday.setText(str(self.i_consum))
        print(self.str_currentDatabase)
        db.insert_Consum(self.i_consum, self.str_currentDatabase)
        consumlogger.info("Consumcounter: " + str(self.i_consum))


    #---- Read Data ------------------------------------------------------------


    def loadData(self):
        #print('load data')                                                         #load data for the Homepage
        data = db.read_consum()
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
        consumlogger.info("Load data Admin: Succesfully")


    #---- Write Data -----------------------------------------------------------

    def createDatabase(self):
        name = self.ui.LE_NameDatabase.text()
        print('Start', name, str(name), type(name))
        if name == "" or name == " ":
            print('fail')
            consumlogger.info("Creating Database failed: No item selected")
            self.L_InputDataFail.setText('Bitte einen Namen eingeben')
        else:
            print('siccess')
            db.newDatabase(name)
            self.init_ComboBox_Database()
            consumlogger.info("Create Database: " + name )
            self.L_InputDataFail.setText('')

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
