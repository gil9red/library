#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mainwindow_ui import Ui_MainWindow
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtSql import *


def create_connection():
    # Открытие базы данных
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('library.db')
    if not db.open():
        db.lastError().showMessage()
        return False

    return True


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.docsModel = QSqlTableModel()
        self.docsModel = QSqlRelationalTableModel()
        self.docsModel.setTable('DOCUMENTS')
        self.docsModel.setRelation(2, QSqlRelation('THEMES', 'ID', 'NAME'))
        self.docsModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.docsModel.select()
        self.docsModel.setHeaderData(1, Qt.Horizontal, "Путь к файлу")
        self.docsModel.setHeaderData(2, Qt.Horizontal, "Тема")

        self.ui.docsView.setModel(self.docsModel)
        self.ui.docsView.setItemDelegate(QSqlRelationalDelegate(self.ui.docsView))
        self.ui.docsView.horizontalHeader().setStretchLastSection(True)

        self.updateThemes()

        self.ui.themes.header().setStretchLastSection(True)
        self.ui.themes.setHeaderHidden(True)
        self.ui.themes.itemSelectionChanged.connect(self.themes_selectionChanged)
        self.ui.themes.setCurrentItem(self.root_theme)

        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAdd.triggered.connect(self.add)
        self.ui.actionDelete.triggered.connect(self.delete)

        self.read_settings()

    def themes_selectionChanged(self):
        item = self.ui.themes.currentItem()
        if item:
            if item is self.root_theme:
                self.docsModel.setFilter(None)
            else:
                pid = item.data(0, Qt.UserRole)[0]
                self.docsModel.setFilter('ID_THEME = {}'.format(pid))

    def updateThemes(self):
        self.ui.themes.clear()

        self.root_theme = QTreeWidgetItem(['Все темы'])
        self.ui.themes.addTopLevelItem(self.root_theme)

        query = QSqlQuery()
        query.exec_('SELECT ID, NAME FROM THEMES')

        while query.next():
            pid = query.value(0)
            name = query.value(1)

            child = QTreeWidgetItem([name])
            child.setData(0, Qt.UserRole, [pid, name])
            self.root_theme.addChild(child)

        self.ui.themes.expandAll()

    def add(self):
        pass

    def delete(self):
        pass

    def read_settings(self):
        ini = QSettings('settings.ini')
        self.restoreGeometry(ini.value('MainWindow_Geometry'))
        self.restoreState(ini.value('MainWindow_State'))
        self.ui.splitter.restoreState(ini.value('Splitter_State'))

    def write_settings(self):
        ini = QSettings('settings.ini')
        ini.setValue('MainWindow_State', self.saveState())
        ini.setValue('MainWindow_Geometry', self.saveGeometry())
        ini.setValue('Splitter_State', self.ui.splitter.saveState())

    def closeEvent(self, *args, **kwargs):
        self.write_settings()

        super().closeEvent(*args, **kwargs)