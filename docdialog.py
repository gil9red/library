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

        # TODO: добавить возможность из диалога создавать / удалять темы
        # TODO: возможность удалять / создавать темы и в главном окне

        query = QSqlQuery()
        query.exec_('SELECT ID, NAME FROM THEMES')

        while query.next():
            pid = query.value(0)
            name = query.value(1)

            self.ui.theme.addItem(name, [pid, name])

        self.ui.theme.setCurrentIndex(0)

    def accept(self, *args, **kwargs):
        query = QSqlQuery()
        query.prepare("INSERT INTO DOCUMENTS (PATH, THEME, NAME, AUTHOR, "
                      "YEAR, ANNOTATION, TABLEOFCONTENTS, BIBLIOGRAPHY) "
                      "VALUES (:PATH, :THEME, :NAME, :AUTHOR, :YEAR ,:ANNOTATION, "
                      ":TABLEOFCONTENTS, :BIBLIOGRAPHY)")

        query.bindValue(":PATH", self.ui.docFileName.text())
        query.bindValue(":THEME", self.ui.theme.currentText())
        query.bindValue(":NAME", self.ui.name.text())
        query.bindValue(":AUTHOR", self.ui.author.text())
        query.bindValue(":YEAR", self.ui.year.value())
        query.bindValue(":ANNOTATION", self.ui.annotation.toHtml())
        query.bindValue(":TABLEOFCONTENTS", self.ui.annotation.toHtml())
        query.bindValue(":BIBLIOGRAPHY", self.ui.annotation.toHtml())

        if not query.exec_():
            text = 'Произошла ошибка при выполнении запроса:\n{}'.format(query.lastError())
            QMessageBox.warning('Внимание', text)

        super().accept(*args, **kwargs)