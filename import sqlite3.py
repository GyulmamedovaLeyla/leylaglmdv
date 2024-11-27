import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from tovari3 import Ui_MainWindow
from izmenitovar import Ui_Dialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)
        
        self.dialog = QtWidgets.QDialog()
        self.ui_dialog = Ui_Dialog()
        self.ui_dialog.setupUi(self.dialog)
        
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Товары' ''')
        result = self.cursor.fetchone()

        self.ui_main.pushButton_8.clicked.connect(self.show_dialog)
        self.ui_main.tableWidget.itemClicked.connect(self.select_item)
        self.ui_main.pushButton_9.clicked.connect(self.show_add_dialog)
        self.ui_main.pushButton_2.clicked.connect(self.delete_item)
        self.display_data_in_table()

    def show_dialog(self):
        self.dialog.show()

    def fill_dialog_with_item(self, item):
        row = item.row()
        code = self.ui_main.tableWidget.item(row, 0).text()
        name = self.ui_main.tableWidget.item(row, 1).text()
        category = self.ui_main.tableWidget.item(row, 2).text()
        price = self.ui_main.tableWidget.item(row, 3).text()
        quantity = self.ui_main.tableWidget.item(row, 4).text()

        self.ui_dialog.lineEdit.setText(code)
        self.ui_dialog.lineEdit_5.setText(name)
        self.ui_dialog.comboBox.setCurrentText(category)
        self.ui_dialog.lineEdit_8.setText(price)
        self.ui_dialog.lineEdit_7.setText(quantity)

    def save_and_close_edit_dialog(self):
        code = self.ui_dialog.lineEdit.text()
        name = self.ui_dialog.lineEdit_5.text()
        category = self.ui_dialog.comboBox.currentText()
        price = float(self.ui_dialog.lineEdit_8.text())
        quantity = float(self.ui_dialog.lineEdit_7.text())

        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            row = selected_item.row()
            old_code = self.ui_main.tableWidget.item(row, 0).text()

            self.cursor.execute('''UPDATE Товары SET Код=?, Наименование=?, Категория=?, Цена=?, Количество=?
                                   WHERE Код=?''', (code, name, category, price, quantity, old_code))
        else:
            self.cursor.execute('''INSERT INTO Товары (Код, Наименование, Категория, Цена, Количество)
                                   VALUES (?, ?, ?, ?, ?)''', (code, name, category, price, quantity))

        self.connection.commit()
        self.dialog.close()
        self.display_data_in_table()

    def display_data_in_table(self):
        self.ui_main.tableWidget.clearContents()

        self.cursor.execute("SELECT Код, Наименование, Категория, Цена, Количество FROM Товары")
        data = self.cursor.fetchall()

        self.ui_main.tableWidget.setRowCount(len(data))
        self.ui_main.tableWidget.setColumnCount(len(data[0])) if data else self.ui_main.tableWidget.setColumnCount(0)

        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.ui_main.tableWidget.setItem(row_num, col_num, item)
                if col_num in (0, 3, 4):  # Adjust columns alignment
                    item.setTextAlignment(Qt.AlignCenter)

        # Set columns width
        self.ui_main.tableWidget.setColumnWidth(0, 120) 
        self.ui_main.tableWidget.setColumnWidth(1, 300)
        self.ui_main.tableWidget.setColumnWidth(2, 240)  
        self.ui_main.tableWidget.setColumnWidth(3, 150)  
        self.ui_main.tableWidget.setColumnWidth(4, 198)  

    def closeEvent(self, event):
        self.connection.close()

    def delete_item(self):
        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            self.dialog.close()

    def select_item(self, item):
        self.ui_main.tableWidget.setCurrentItem(item)
