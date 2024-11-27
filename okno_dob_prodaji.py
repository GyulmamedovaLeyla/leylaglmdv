from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(482, 550)
        Dialog.setAcceptDrops(False)
        icon = QtGui.QIcon.fromTheme("Товары")
        Dialog.setWindowIcon(icon)
        Dialog.setWindowOpacity(1.0)
        Dialog.setStyleSheet("background-color: rgb(212, 208, 207);\n"
"background-color: rgb(240, 234, 231);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 481, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(59, 38, 33);\n"
"")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.splitter_2 = QtWidgets.QSplitter(Dialog)
        self.splitter_2.setGeometry(QtCore.QRect(50, 430, 380, 101))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.pushButton = QtWidgets.QPushButton(self.splitter_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pushButton.setObjectName("pushButton")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(10, 50, 211, 350))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label_8 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(59, 38, 33);")
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(59, 38, 33);")
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(59, 38, 33);")
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color: rgb(59, 38, 33);")
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(59, 38, 33);")
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color: rgb(59, 38, 33);")
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.splitter_3 = QtWidgets.QSplitter(Dialog)
        self.splitter_3.setGeometry(QtCore.QRect(240, 55, 231, 340))
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.splitter_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.splitter_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.splitter_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.comboBox_2 = QtWidgets.QComboBox(self.splitter_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.comboBox_2.setMouseTracking(False)
        self.comboBox_2.setObjectName("comboBox_2")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.splitter_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.comboBox_3 = QtWidgets.QComboBox(self.splitter_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.comboBox_3.setMouseTracking(False)
        self.comboBox_3.setObjectName("comboBox_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Загрузка данных из базы данных в QComboBox
        self.load_data_to_combobox()

    def load_data_to_combobox(self):
        # Подключение к базе данных SQLite для таблицы "Товары"
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()

        # Выполнение запроса SELECT для получения данных из таблицы "Товары" для столбцов "Код" и "Наименование"
        cursor.execute("SELECT Код, Наименование FROM Товары")
        rows = cursor.fetchall()

        # Добавление данных в QComboBox
        for row in rows:
            self.comboBox_2.addItem(f"{row[0]}: {row[1]}")  # Комбинированное значение Код и Наименование

        # Закрытие подключения к базе данных
        connection.close()

        # Подключение к базе данных SQLite для таблицы "Сотрудники"
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()

        # Выполнение запроса SELECT для получения данных из таблицы "Сотрудники" для столбцов "ID" и "ФИО"
        cursor.execute("SELECT ID, ФИО FROM Сотрудники")
        rows = cursor.fetchall()

        # Добавление данных в QComboBox
        for row in rows:
            self.comboBox_3.addItem(f"{row[0]}: {row[1]}")  # Комбинированное значение ID и ФИО

        # Закрытие подключения к базе данных
        connection.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Добавить товар"))
        self.label.setText(_translate("Dialog", "Добавить продажу"))
        self.pushButton.setText(_translate("Dialog", "Сохранить"))
        self.label_8.setText(_translate("Dialog", "Номер продажи"))
        self.label_9.setText(_translate("Dialog", "Сумма продажи"))
        self.label_10.setText(_translate("Dialog", "Дата"))
        self.label_11.setText(_translate("Dialog", "Код товара"))
        self.label_12.setText(_translate("Dialog", "Количество"))
        self.label_13.setText(_translate("Dialog", "ID сотрудника"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
