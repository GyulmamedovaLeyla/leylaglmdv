import sqlite3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from prodaji import Ui_MainWindow
from okno_dob_prodaji import Ui_Dialog
from okno_izm_prod import Ui_Dialog as Ui_Dialog_IzmenitProd

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

        # Подключение к базе данных SQLite и загрузка данных из таблицы "Продажи"
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()

        # Загрузка данных из базы данных при запуске
        self.load_data_from_sales()

    def open_add_sale_dialog(self):
        # Создание и отображение диалогового окна для добавления продажи
        self.dialog = QtWidgets.QDialog()
        self.ui_dialog = Ui_Dialog()
        self.ui_dialog.setupUi(self.dialog)
        self.ui_dialog.pushButton.clicked.connect(self.save_sale)  # Обработчик для кнопки "Сохранить"
        self.dialog.show()

    def load_data_from_sales(self):
        # Выполнение запроса SELECT для получения данных из таблицы "Продажи"
        self.cursor.execute("SELECT * FROM Продажи")
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
        self.ui_main.tableWidget.setColumnWidth(0, 250) 
        self.ui_main.tableWidget.setColumnWidth(1, 350)
        self.ui_main.tableWidget.setColumnWidth(2, 310)  
        self.ui_main.tableWidget.setColumnWidth(3, 180)  
        self.ui_main.tableWidget.setColumnWidth(4, 240)  
        self.ui_main.tableWidget.setColumnWidth(5, 265)  

    def save_sale(self):
        sale_number = self.ui_dialog.lineEdit_2.text()
        sale_amount = self.ui_dialog.lineEdit_3.text()
        sale_date = self.ui_dialog.lineEdit_4.text()
        product_code = self.ui_dialog.comboBox_2.currentText()
        quantity = self.ui_dialog.lineEdit_5.text()
        employee_id = self.ui_dialog.comboBox_3.currentText().split(':')[0]

        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO Продажи (Номер_продажи, Сумма_продажи, Дата, Код_товара, Количество, ID_сотрудника) VALUES (?, ?, ?, ?, ?, ?)",
               (sale_number, sale_amount, sale_date, product_code, quantity, employee_id))

        self.connection.commit()

        # Перезагрузка данных после сохранения
        self.load_data_from_sales()

        # Закрытие диалогового окна
        self.dialog.close()

    def show_dialog(self):
        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            self.dialog_okno_izm_prod = QtWidgets.QDialog()
            self.ui_dialog_izm_prod = Ui_Dialog_IzmenitProd()
            self.ui_dialog_izm_prod.setupUi(self.dialog_okno_izm_prod)
            self.fill_dialog_with_item(selected_item)
            self.ui_dialog_izm_prod.pushButton.clicked.connect(self.save_and_close_dialog)  # Подключение кнопки к методу
            self.ui_dialog_izm_prod.pushButton_2.clicked.connect(self.delete_sale)  # Подключение кнопки удаления
            self.dialog_okno_izm_prod.show()

    def fill_dialog_with_item(self, item):
        row = item.row()
        sale_number = self.ui_main.tableWidget.item(row, 0).text()
        sale_amount = self.ui_main.tableWidget.item(row, 1).text()
        sale_date = self.ui_main.tableWidget.item(row, 2).text()
        product_code = self.ui_main.tableWidget.item(row, 3).text()
        quantity = self.ui_main.tableWidget.item(row, 4).text()
        employee_id = self.ui_main.tableWidget.item(row, 5).text()

        self.ui_dialog_izm_prod.lineEdit.setText(sale_number)
        self.ui_dialog_izm_prod.lineEdit_5.setText(sale_amount)
        self.ui_dialog_izm_prod.lineEdit_2.setText(sale_date) 
        self.ui_dialog_izm_prod.comboBox.setCurrentText(product_code)
        self.ui_dialog_izm_prod.lineEdit_8.setText(quantity)
        self.ui_dialog_izm_prod.comboBox_2.setCurrentText(employee_id)

    def save_and_close_dialog(self):
        sale_number = self.ui_dialog_izm_prod.lineEdit.text()
        sale_amount = self.ui_dialog_izm_prod.lineEdit_5.text()
        sale_date = self.ui_dialog_izm_prod.lineEdit_2.text()
        product_code = self.ui_dialog_izm_prod.comboBox.currentText()
        quantity = self.ui_dialog_izm_prod.lineEdit_8.text()
        employee_id = self.ui_dialog_izm_prod.comboBox_2.currentText().split(':')[0]

        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            row = selected_item.row()
            old_code = self.ui_main.tableWidget.item(row, 0).text()

            self.cursor.execute('''UPDATE Продажи SET Номер_продажи=?, Сумма_продажи=?, Дата=?, Код_товара=?, Количество=?, ID_сотрудника=?
                                   WHERE Номер_продажи=?''', (sale_number, sale_amount, sale_date, product_code, quantity, employee_id, old_code))
        else:
            self.cursor.execute('''INSERT INTO Продажи (Номер_продажи, Сумма_продажи, Дата, Код_товара, Количество, ID_сотрудника)
                                   VALUES (?, ?, ?, ?, ?, ?)''', (sale_number, sale_amount, sale_date, product_code, quantity, employee_id))

        self.connection.commit()
        self.dialog_okno_izm_prod.close()
        self.load_data_from_sales()

    def delete_sale(self):
        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            sale_number = selected_item.text()
            self.cursor.execute("DELETE FROM Продажи WHERE Номер_продажи=?", (sale_number,))
            self.connection.commit()
            self.load_data_from_sales()

    def closeEvent(self, event):
        # Закрытие подключения к базе данных при закрытии приложения
        self.connection.close()
   
def close_and_return_to_main_window(self):
        self.close()
        main_window = MainWindow()
        main_window.show()
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()