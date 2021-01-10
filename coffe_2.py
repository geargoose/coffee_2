import sqlite3
import sys

from PyQt5 import QtCore, QtWidgets


class DBHelper:
    def __init__(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.genre_id, self.id_genre = {}, {}
        self.get_genres()

    def add_to_films(self, name, year, genre, duration):
        self.cur.execute(
            f"INSERT INTO films (id, title, year, genre, duration) values "
            f"((select max(id) from films) + 1, '{name}', {year}, '{genre}', {duration})")
        self.con.commit()

    def get_genres(self):
        genre_id = {}
        id_genre = {}
        result = self.cur.execute('select * from genres')
        for id_, genre in list(result):
            genre_id[genre] = id_
            id_genre[id_] = genre
        self.genre_id, self.id_genre = genre_id, id_genre
        return self.cur.execute('select * from genres')

    def get_films_row(self, id):
        result = self.cur.execute(f"select * from films where id = {id}").fetchone()
        return result

    def get_films(self):
        films = self.cur.execute('select * from films')
        return films

    def edit_film(self, id, name, year, genre, duration):
        self.cur.execute(f"update films set "
                         f"title = '{name}', "
                         f"year = {year}, "
                         f"genre = {genre},"
                         f"duration = {duration} where id = {id}")
        self.con.commit()

    def delete_film(self, id_):
        self.cur.execute(f"delete from films where id = {id_}")
        self.con.commit()

    def add_to_genres(self, title):
        self.cur.execute(f"INSERT INTO genres (id, title) values "
                         f"((select max(id) from genres) + 1, '{title}')")

    def edit_genre(self, id, title):
        self.cur.execute(f"update genres set "
                         f"title = '{title}' where id = {id}")
        self.con.commit()

    def get_genres_row(self, id):
        result = self.cur.execute(f"select * from genres where id = {id}").fetchone()
        return result

    def delete_genre(self, id_):
        self.cur.execute(f"delete from genres where id = {id_}")
        self.con.commit()

    def delete_film_by_genre(self, genre):
        self.cur.execute(f"delete from films where genre = {genre}")


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(321, 176)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название"))
        self.pushButton.setText(_translate("Form", "Добавить"))


class AddGenreDialog(QtWidgets.QDialog, Ui_Form):
    def __init__(self, helper: DBHelper):
        super().__init__()
        self.helper = helper
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_genre)

    def add_genre(self):
        title = self.lineEdit.text()
        if len(title) != 0:
            self.helper.add_to_genres(title)
            self.close()
        else:
            pass


class EditGenreDialog(QtWidgets.QDialog, Ui_Form):
    def __init__(self, helper: DBHelper, id, genre):
        super().__init__()
        self.helper = helper
        self.id = id
        self.setupUi(self)
        self.lineEdit.setText(genre)
        self.pushButton.setText('Изменить')
        self.pushButton.clicked.connect(self.edit)

    def edit(self):
        title = self.lineEdit.text()
        if len(title) != 0:
            self.helper.edit_genre(self.id, title)
            self.close()
        else:
            pass


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(384, 233)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_warn = QtWidgets.QLabel()
        self.horizontalLayout.addWidget(self.label_warn)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название"))
        self.label_2.setText(_translate("Form", "Цена"))
        self.label_3.setText(_translate("Form", "Обжарка"))
        self.label_4.setText(_translate("Form", "Вес"))
        self.pushButton.setText(_translate("Form", "Добавить"))


class EditFilmDialog(QtWidgets.QDialog, Ui_Form):
    def __init__(self, helper: DBHelper, id, title, year, genre, duration):
        super().__init__()
        self.setupUi(self)
        self.helper = helper

        self.id = id
        self.title = title
        self.year = year
        self.genre = genre
        self.duration = duration

        self.lineEdit.setText(title)
        self.lineEdit_2.setText(str(year))
        self.comboBox.addItems(self.helper.genre_id.keys())
        self.lineEdit_3.setText(str(duration))

        self.comboBox.setCurrentIndex(self.helper.genre_id[genre] - 1)
        self.pushButton.setText("Изменить")
        self.pushButton.clicked.connect(self.edit)

    def edit(self):
        try:
            id = int(self.id)
            title = self.lineEdit.text()
            if len(title) == 0:
                raise ValueError
            year = int(self.lineEdit_2.text())
            genre = self.helper.genre_id[self.comboBox.currentText()]
            duration = int(self.lineEdit_3.text())
            self.helper.edit_film(id, title, year, genre, duration)
            self.close()
        except Exception as e:
            print(e)
            pass


class AddFilmDialog(QtWidgets.QDialog, Ui_Form):
    def __init__(self, helper: DBHelper):
        super().__init__()
        self.setupUi(self)
        self.helper = helper
        self.comboBox.addItems(self.helper.genre_id.keys())
        self.pushButton.clicked.connect(self.add_to_db)

    def add_to_db(self):
        try:
            name = self.lineEdit.text()
            if len(name) == 0:
                raise ValueError
            year = int(self.lineEdit_2.text())
            genre = self.helper.genre_id[self.comboBox.currentText()]
            duration = int(self.lineEdit_3.text())
            self.helper.add_to_films(name, year, genre, duration)
            self.close()
        except ValueError as e:
            print(e)
            self.label_warn.setText('Некорректные данные')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Добавить вид кофе"))
        self.pushButton_2.setText(_translate("MainWindow", "Редактировать вид кофе"))
        self.pushButton_3.setText(_translate("MainWindow", "Удалить вид кофе"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Виды кофе"))
        self.pushButton_4.setText(_translate("MainWindow", "Добавить обжарку"))
        self.pushButton_5.setText(_translate("MainWindow", "Редактировать обжарку"))
        self.pushButton_6.setText(_translate("MainWindow", "Удалить обжарку"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Обжарка"))


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.helper = DBHelper()
        self.con = sqlite3.connect("films_db.sqlite")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.add_film_dialog)
        self.pushButton_2.clicked.connect(self.edit_film_dialog)
        self.pushButton_3.clicked.connect(self.delete_film)
        self.pushButton_4.clicked.connect(self.add_genre_dialog)
        self.pushButton_5.clicked.connect(self.edit_genre_dialog)
        self.pushButton_6.clicked.connect(self.delete_genre)
        self.update_all()

    def update_all(self):
        self.update_films_table()
        self.update_genres_table()

    def add_film_dialog(self):
        dialog = AddFilmDialog(self.helper)
        dialog.exec()
        self.update_films_table()

    def edit_film_dialog(self):
        selected_items = self.tableWidget.selectedItems()
        if len(selected_items) != 0:
            selected_row = selected_items[0].row()
        else:
            return

        cols = self.tableWidget.columnCount()
        items = [item.text() for item in [self.tableWidget.item(selected_row, i) for i in range(cols)]]
        dialog = EditFilmDialog(self.helper, *items)
        dialog.exec()
        for j, elem in enumerate(self.helper.get_films_row(int(items[0]))):
            if j == 3:
                elem = self.helper.id_genre[elem]
            self.tableWidget.item(selected_row, j).setText(str(elem))
        # self.update_films_table()

    def delete_film(self):
        confirmation = QtWidgets.QMessageBox.question(self, 'Подтверждение действия', 'Действительно удалить?',
                                                      QtWidgets.QMessageBox.Yes,
                                                      QtWidgets.QMessageBox.No)
        if confirmation == QtWidgets.QMessageBox.Yes:
            selected_items = self.tableWidget.selectedItems()
            if len(selected_items) != 0:
                selected_row = selected_items[0].row()
            else:
                return
            id_ = int(self.tableWidget.item(selected_row, 0).text())
            self.helper.delete_film(id_)
            self.tableWidget.removeRow(selected_row)

    def update_films_table(self):
        films = self.helper.get_films()
        headers = ['ID', 'Название', 'Цена', 'Обжарка', 'Вес']
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(headers)

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(films):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    elem = self.helper.id_genre[elem]
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(elem)))

    def update_genres_table(self):
        genres = self.helper.get_genres()
        headers = ['ID', 'Название']
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setHorizontalHeaderLabels(headers)
        self.tableWidget_2.setRowCount(0)
        for i, row in enumerate(genres):
            self.tableWidget_2.setRowCount(self.tableWidget_2.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(elem)))

    def add_genre_dialog(self):
        dialog = AddGenreDialog(self.helper)
        dialog.exec()
        self.update_genres_table()

    def edit_genre_dialog(self):
        selected_items = self.tableWidget_2.selectedItems()
        if len(selected_items) != 0:
            selected_row = selected_items[0].row()
        else:
            return

        cols = self.tableWidget_2.columnCount()
        items = [item.text() for item in [self.tableWidget_2.item(selected_row, i) for i in range(cols)]]
        dialog = EditGenreDialog(self.helper, *items)
        dialog.exec()
        self.helper.get_genres()
        self.update_all()

    def delete_genre(self):
        confirmation = QtWidgets.QMessageBox.question(self, 'Подтверждение действия',
                                                      'Будут удалены все виды кофе с такой обжаркой.\nПродолжить?',
                                                      QtWidgets.QMessageBox.Yes,
                                                      QtWidgets.QMessageBox.No)
        if confirmation == QtWidgets.QMessageBox.Yes:
            selected_items = self.tableWidget_2.selectedItems()
            if len(selected_items) != 0:
                selected_row = selected_items[0].row()
            else:
                return
            id_ = int(self.tableWidget_2.item(selected_row, 0).text())
            self.helper.delete_film_by_genre(id_)
            self.helper.delete_genre(id_)
            self.tableWidget_2.removeRow(selected_row)
            self.update_all()


def excepthook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    sys.__excepthook__ = excepthook
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
