import sqlite3
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from tovari3 import Ui_MainWindow
from okno import Ui_Dialog
from kategory import Ui_Dialog as Ui_Dialog_Categories
from kategory_do import Ui_Dialog as Ui_Dialog_AddCategory
from izmenitovar import Ui_Dialog as Ui_Dialog_Izmenit
from prodaji_okno import MainWindow as ProdajiWindow  # Импортируем класс для окна продаж
from sotrudniki_okno import MainWindow as SotrudnikiWindow
from okno_otcet import MainWindow as OtcetWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)

        self.dialog = QtWidgets.QDialog()
        self.ui_dialog = Ui_Dialog()
        self.ui_dialog.setupUi(self.dialog)
        
        self.dialog_categories = QtWidgets.QDialog()
        self.ui_dialog_categories = Ui_Dialog_Categories()
        self.ui_dialog_categories.setupUi(self.dialog_categories)

        self.dialog_add_category = QtWidgets.QDialog()
        self.ui_dialog_add_category = Ui_Dialog_AddCategory()
        self.ui_dialog_add_category.setupUi(self.dialog_add_category)

        self.dialog_izmenit = QtWidgets.QDialog()
        self.ui_dialog_izmenit = Ui_Dialog_Izmenit()
        self.ui_dialog_izmenit.setupUi(self.dialog_izmenit)
    
        # Подключение функции к кнопке на главном окне
        self.ui_main.pushButton_8.clicked.connect(self.show_dialog)
        
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Товары' ''')
        result = self.cursor.fetchone()

        self.ui_main.tableWidget.itemClicked.connect(self.select_item)
        
        self.display_data_in_table()  
        self.ui_main.pushButton_9.clicked.connect(self.show_add_dialog)
        self.ui_dialog.pushButton.clicked.connect(self.save_and_close_edit_dialog)

        self.ui_main.pushButton_5.clicked.connect(self.show_categories_dialog)
        self.ui_dialog_categories.pushButton.clicked.connect(self.show_add_category_dialog)
        self.ui_dialog_add_category.pushButton_3.clicked.connect(self.save_category_changes)
        self.ui_dialog_add_category.pushButton_4.clicked.connect(self.close_add_category_dialog)
        self.ui_dialog_categories.pushButton_2.clicked.connect(self.delete_category)

        self.ui_dialog_izmenit.pushButton.clicked.connect(self.save_and_close_dialog)
        self.ui_dialog_izmenit.pushButton_2.clicked.connect(self.delete_item)  # Добавлено подключение кнопки "Удалить товар" на диалоговом окне "Изменить товар"


        self.window_mapping = {
            self.ui_main.pushButton_2: self.open_prodaji_okno,
            self.ui_main.pushButton_3: self.open_sotrudniki_okno,
            self.ui_main.pushButton_4: self.open_okno_otcet
        }

        for button, method in self.window_mapping.items():
            button.clicked.connect(method)


#Нажатие на "Продажи"
        self.ui_main.pushButton_2.clicked.connect(self.open_prodaji_okno)

    def open_prodaji_okno(self):
        self.prodaji_okno = ProdajiWindow()
        self.prodaji_okno.show()

        self.display_data_in_table()

#Нажатие на "Сотрудники"
        self.ui_main.pushButton_3.clicked.connect(self.open_sotrudniki_okno)

    def open_sotrudniki_okno(self):
        self.sotrudniki_okno = SotrudnikiWindow()
        self.sotrudniki_okno.show()

        self.display_data_in_table()

#Нажатие на "Отчёты"
        self.ui_main.pushButton_4.clicked.connect(self.open_okno_otcet)

    def open_okno_otcet(self):
        self.okno_otcet = OtcetWindow()
        self.okno_otcet.show()

        self.display_data_in_table()

    # Товары
    def show_add_dialog(self):
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
                if col_num == 0:  
                    item.setTextAlignment(Qt.AlignCenter)
                if col_num == 3:  
                    item.setTextAlignment(Qt.AlignCenter)
                if col_num == 4:  
                    item.setTextAlignment(Qt.AlignCenter)
        
        # Задаём ширину столбцов
        self.ui_main.tableWidget.setColumnWidth(0, 180) 
        self.ui_main.tableWidget.setColumnWidth(1, 450)
        self.ui_main.tableWidget.setColumnWidth(2, 370)  
        self.ui_main.tableWidget.setColumnWidth(3, 240)  
        self.ui_main.tableWidget.setColumnWidth(4, 343)  

    def closeEvent(self, event):
        self.connection.close()

    def delete_item(self):
        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            row = selected_item.row()
            code = self.ui_main.tableWidget.item(row, 0).text()

            # Удаление товара из базы данных
            self.cursor.execute('''DELETE FROM Товары WHERE Код=?''', (code,))
            self.connection.commit()

            # Обновление данных в TableWidget на главном окне
            self.display_data_in_table()
            self.dialog_izmenit.close()

    def select_item(self, item):
        self.ui_main.tableWidget.setCurrentItem(item)
    # Категории
    def show_categories_dialog(self):
        self.load_categories()
        self.dialog_categories.show()

    def show_add_category_dialog(self):
        self.dialog_add_category.show()

    def load_categories(self):
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()

        cursor.execute("SELECT ID, Название FROM Категории")
        categories = cursor.fetchall()

        self.ui_dialog_categories.tableWidget.setRowCount(len(categories))
        self.ui_dialog_categories.tableWidget.setColumnCount(len(categories[0]))
        
        for row_num, row_data in enumerate(categories):
            for col_num, col_data in enumerate(row_data):
                self.ui_dialog_categories.tableWidget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data)))

    def save_category_changes(self):
        new_category = self.ui_dialog_add_category.lineEdit.text()
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO Категории (Название) VALUES (?)", (new_category,))
        connection.commit()
        connection.close()

        self.load_categories()
        self.dialog_add_category.close()  # Закрываем диалоговое окно после сохранения изменений

    def close_add_category_dialog(self):
        self.dialog_add_category.close()  # Закрываем диалоговое окно без сохранения изменений

    def delete_category(self):
        selected_item = self.ui_dialog_categories.tableWidget.currentItem()
        if selected_item:
            row = selected_item.row()
            category_id = self.ui_dialog_categories.tableWidget.item(row, 0).text()
            connection = sqlite3.connect('example.db')
            cursor = connection.cursor()

            cursor.execute("DELETE FROM Категории WHERE ID=?", (category_id,))
            connection.commit()
            connection.close()

            self.load_categories()

    # Изменить
    def show_dialog(self):
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Товары' ''')
       

        self.ui_main.tableWidget.itemClicked.connect(self.select_item)
    
        selected_item = self.ui_main.tableWidget.currentItem()
        if selected_item:
            self.fill_dialog_with_item(selected_item)
            self.dialog_izmenit.show()

    def fill_dialog_with_item(self, item):
        
        row = item.row()
        code = self.ui_main.tableWidget.item(row, 0).text()
        name = self.ui_main.tableWidget.item(row, 1).text()
        category = self.ui_main.tableWidget.item(row, 2).text()
        price = self.ui_main.tableWidget.item(row, 3).text()
        quantity = self.ui_main.tableWidget.item(row, 4).text()

        self.ui_dialog_izmenit.lineEdit.setText(code)
        self.ui_dialog_izmenit.lineEdit_5.setText(name)
        self.ui_dialog_izmenit.comboBox.setCurrentText(category)
        self.ui_dialog_izmenit.lineEdit_8.setText(price)
        self.ui_dialog_izmenit.lineEdit_7.setText(quantity)
        
        self.ui_dialog_izmenit.pushButton.clicked.connect(self.save_and_close_dialog)
        

    def save_and_close_dialog(self):
        code = self.ui_dialog_izmenit.lineEdit.text()
        name = self.ui_dialog_izmenit.lineEdit_5.text()
        category = self.ui_dialog_izmenit.comboBox.currentText()
        price = float(self.ui_dialog_izmenit.lineEdit_8.text())
        quantity = float(self.ui_dialog_izmenit.lineEdit_7.text())

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
        self.dialog_izmenit.close()
        self.display_data_in_table()

        # Очищаем событие, чтобы избежать множественных соединений
        self.ui_dialog_izmenit.pushButton.disconnect()

        self.ui_dialog_izmenit.pushButton_2.clicked.connect(self.delete_item)
        
def delete_item(self):
    selected_item = self.ui_main.tableWidget.currentItem()
    if selected_item:
        row = selected_item.row()
        code = self.ui_main.tableWidget.item(row, 0).text()

        # Удаляем товар из базы данных
        self.cursor.execute('''DELETE FROM Товары WHERE Код=?''', (code,))
        self.connection.commit()

        # Закрываем диалог и принимаем изменения
        self.dialog_izmenit.close()
        

        # Обновляем отображение данных в таблице на главном экране
        self.display_data_in_table()
        
def open_main_window(self):
        self.show()  #встпавлено 
              
               
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()