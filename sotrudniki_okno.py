import sqlite3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from sotrudniki import Ui_MainWindow
from okno_dob_sotr import Ui_Dialog
from okno_izm_sotr import Ui_Dialog as Ui_Dialog_IzmenitSotr

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)

        # Подключение обработчика события для кнопки "Добавить"
        self.ui_main.pushButton_9.clicked.connect(self.open_add_sale_dialog)
        # Подключение обработчика события для кнопки "Изменить"
        self.ui_main.pushButton_8.clicked.connect(self.show_dialog)
        #Кнопка назад
        self.ui_main.pushButton_6.clicked.connect(self.close)

        # Подключение к базе данных SQLite и загрузка данных из таблицы "Сотрудники"
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()

        # Загрузка данных из базы данных при запуске
        self.load_data_from_sotrudniki()

    def open_add_sale_dialog(self):
        # Создание и отображение диалогового окна для добавления сотрудника
        self.dialog = QtWidgets.QDialog()
        self.ui_dialog = Ui_Dialog()
        self.ui_dialog.setupUi(self.dialog)
        self.ui_dialog.pushButton.clicked.connect(self.save_sale)  # Обработчик для кнопки "Сохранить"
        self.dialog.show()

    def load_data_from_sotrudniki(self):
        # Выполнение запроса SELECT для получения данных из таблицы "Сотрудники"
        self.cursor.execute("SELECT * FROM Сотрудники")
        rows = self.cursor.fetchall()

        # Загрузка данных в TableWidget
        self.ui_main.tableWidget.setRowCount(len(rows))
        self.ui_main.tableWidget.setColumnCount(len(rows[0])) if rows else self.ui_main.tableWidget.setColumnCount(0)

        for row_num, row_data in enumerate(rows):
            for col_num, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.ui_main.tableWidget.setItem(row_num, col_num, item)
                item.setTextAlignment(Qt.AlignCenter)  # Выравнивание по центру

        # Задаём ширину столбцов
        self.ui_main.tableWidget.setColumnWidth(0, 180) 
        self.ui_main.tableWidget.setColumnWidth(1, 600)
        self.ui_main.tableWidget.setColumnWidth(2, 362)  
        self.ui_main.tableWidget.setColumnWidth(3, 450)  
       

    def save_sale(self):
        ID = self.ui_dialog.lineEdit_2.text()
        fio = self.ui_dialog.lineEdit_3.text()
        contact_information = self.ui_dialog.lineEdit_4.text()
        residential_address = self.ui_dialog.lineEdit_5.text()
        

        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO Сотрудники (ID, ФИО, Контактные_данные, Адрес_проживания) VALUES (?, ?, ?, ?)",
               (ID, fio, contact_information, residential_address))

        self.connection.commit()

        # Перезагрузка данных после сохранения
        self.load_data_from_sotrudniki()

        # Закрытие диалогового окна
        self.dialog.close()

    def show_dialog(self):
        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            self.dialog_okno_izm_sotr = QtWidgets.QDialog()
            self.ui_dialog_izm_sotr = Ui_Dialog_IzmenitSotr()
            self.ui_dialog_izm_sotr.setupUi(self.dialog_okno_izm_sotr)
            self.fill_dialog_with_item(selected_item)
            self.ui_dialog_izm_sotr.pushButton.clicked.connect(self.save_and_close_dialog)  # Подключение кнопки к методу
            self.ui_dialog_izm_sotr.pushButton_2.clicked.connect(self.delete_sale)  # Подключение кнопки удаления
            self.dialog_okno_izm_sotr.show()

    def fill_dialog_with_item(self, item):
        row = item.row()
        ID = self.ui_main.tableWidget.item(row, 0).text()
        fio = self.ui_main.tableWidget.item(row, 1).text()
        contact_information = self.ui_main.tableWidget.item(row, 2).text()
        residential_address = self.ui_main.tableWidget.item(row, 3).text()
    

        self.ui_dialog_izm_sotr.lineEdit.setText(ID)
        self.ui_dialog_izm_sotr.lineEdit_5.setText(fio)
        self.ui_dialog_izm_sotr.lineEdit_2.setText(contact_information) 
        self.ui_dialog_izm_sotr.lineEdit_8.setText(residential_address)
        
    def save_and_close_dialog(self):
        ID = self.ui_dialog_izm_sotr.lineEdit.text()
        fio = self.ui_dialog_izm_sotr.lineEdit_5.text()
        contact_information = self.ui_dialog_izm_sotr.lineEdit_2.text()
        residential_address = self.ui_dialog_izm_sotr.lineEdit_8.text()
 

        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            row = selected_item.row()
            old_code = self.ui_main.tableWidget.item(row, 0).text()

            self.cursor.execute('''UPDATE Сотрудники SET ID=?, ФИО=?, Контактные_данные=?, Адрес_проживания=?
                                   WHERE ID=?''', (ID, fio, contact_information, residential_address, old_code))
        else:
            self.cursor.execute('''INSERT INTO Сотрудники (ID, ФИО, Контактные_данные, Адрес_проживания)
                                   VALUES (?, ?, ?, ?, ?)''', (ID, fio, contact_information, residential_address))

        self.connection.commit()
        self.dialog_okno_izm_sotr.close()
        self.load_data_from_sotrudniki()

    def delete_sale(self):
        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            row = selected_item.row()
            ID = self.ui_main.tableWidget.item(row, 0).text()
            self.cursor.execute("DELETE FROM Сотрудники WHERE ID=?", (ID,))
            self.connection.commit()
            self.load_data_from_sotrudniki()

    def closeEvent(self, event):
        # Закрытие подключения к базе данных при закрытии приложения
        self.connection.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()