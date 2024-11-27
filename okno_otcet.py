from PyQt5 import QtCore, QtWidgets
from otcet import Ui_MainWindow
from form_otcet import Ui_Dialog

import sqlite3

class ReportDialog(QtWidgets.QDialog):
    report_ready = QtCore.pyqtSignal(list)  # Определить сигнал для передачи данных

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Установка формата даты для dateEdit и dateEdit_2
        date_format = "dd.MM.yyyy"
        self.ui.dateEdit.setDisplayFormat(date_format)
        self.ui.dateEdit_2.setDisplayFormat(date_format)

        self.ui.pushButton_2.clicked.connect(self.generate_report)

    def generate_report(self):
        start_date = self.ui.dateEdit.date().toString("dd.MM.yyyy")
        end_date = self.ui.dateEdit_2.date().toString("dd.MM.yyyy")

        # Запрос SQL для получения общей суммы продаж за указанный период
        query = "SELECT SUM(Сумма_продажи) AS Общая_сумма_продаж FROM Продажи WHERE Дата BETWEEN ? AND ?"
        
        connection = sqlite3.connect("example.db")
        cursor = connection.cursor()

        try:
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            self.close()  # Закрыть диалоговое окно
            self.report_ready.emit(results)  # Отправить сигнал с результатами отчета
        except Exception as e:
            print("Error executing query:", e)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_8.clicked.connect(self.open_dialog)
        # Кнопка назад
        self.pushButton_6.clicked.connect(self.close)

    def open_dialog(self):
        self.dialog = ReportDialog()
        self.dialog.report_ready.connect(self.display_report)  # Связать сигнал с обработчиком
        self.dialog.show()

    def display_report(self, results):
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Начальная дата", "Конечная дата", "Общая сумма продаж"])
        
        # Установка фиксированной ширины столбцов
        self.tableWidget.setColumnWidth(0, 500)
        self.tableWidget.setColumnWidth(1, 500)
        self.tableWidget.setColumnWidth(2, 596)

        # Добавляем начальную и конечную дату
        start_date = self.dialog.ui.dateEdit.date().toString("dd.MM.yyyy")
        end_date = self.dialog.ui.dateEdit_2.date().toString("dd.MM.yyyy")

        item_start_date = QtWidgets.QTableWidgetItem(start_date)
        item_end_date = QtWidgets.QTableWidgetItem(end_date)
        item_total_sales = QtWidgets.QTableWidgetItem(str(results[0][0]))

        # Установка выравнивания текста по центру для каждой ячейки таблицы
        item_start_date.setTextAlignment(QtCore.Qt.AlignCenter)
        item_end_date.setTextAlignment(QtCore.Qt.AlignCenter)
        item_total_sales.setTextAlignment(QtCore.Qt.AlignCenter)

        self.tableWidget.setItem(0, 0, item_start_date)
        self.tableWidget.setItem(0, 1, item_end_date)
        self.tableWidget.setItem(0, 2, item_total_sales)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
