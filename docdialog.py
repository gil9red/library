#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docdialog_ui import Ui_Dialog
from PySide.QtGui import *
from PySide.QtSql import QSqlQuery


class DocDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        query = QSqlQuery()
        query.exec_('SELECT ID, NAME FROM THEMES')

        while query.next():
            pid = query.value(0)
            name = query.value(1)

            self.ui.theme.addItem(name, [pid, name])

        self.ui.theme.setCurrentIndex(0)