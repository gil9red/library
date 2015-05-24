#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import sys

from mainwindow import *


if __name__ == '__main__':
    app = QApplication(sys.argv)

    if not create_connection():
        sys.exit(1)

    query = QSqlQuery()
    # query.exec_('.tables')
    # print(query.result())
    # query.exec_('CREATE TABLE Documents ('
    #             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    #             'path TEXT NOT NULL,'  # путь к документу
    #             'references TEXT,'  # использованная литература
    #             'author TEXT,'  # автор
    #             'year INTEGER,'  # год
    #             'annotation TEXT,'  # аннотация
    #             'contents TEXT'  # содержание
    #             ');')


    query.exec_('DROP TABLE DOCUMENTS')
    #
    # # Тема работы (монография, работа в журнале, и т.п.)
    # query.exec_('CREATE TABLE THEMES('
    #             'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
    #             'NAME TEXT NOT NULL'
    #             ');')

    query.exec_('CREATE TABLE DOCUMENTS('
                'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                'PATH       TEXT    NOT NULL,'  # Путь к файлу работы
                'ID_THEME INTEGER,'  # Тема работы
                'NAME TEXT,'  # Название работы
                'AUTHOR TEXT,'  # Автор
                'YEAR TEXT,'  # Год издания
                'ANNOTATION TEXT,'  # Аннотация
                'TABLEOFCONTENTS TEXT,'  # Оглавление
                'REFERENCES TEXT'  # Список литературы
                'FOREIGN KEY(ID_THEME) REFERENCES THEMES(ID)'
                ');')


    # print(query.lastError())

    # query.exec_("INSERT INTO THEMES (NAME) VALUES ('Монография')")
    # query.exec_("INSERT INTO THEMES (NAME) VALUES ('Журналы')")
    # print(query.lastError())

    # query.exec_("INSERT INTO DOCUMENTS (PATH, ID_THEME) VALUES ('doc.doc', '2')")
    # query.exec_("INSERT INTO DOCUMENTS (PATH, ID_THEME) VALUES ('doc2.doc', '1')")
    # query.exec_("INSERT INTO DOCUMENTS (PATH, ID_THEME) VALUES ('doc3.doc', '2')")
    # print(query.lastError())


    # QSqlQuery query;
    # query.prepare("INSERT INTO person (id, forename, surname) "
    #               "VALUES (:id, :forename, :surname)");
    # query.bindValue(":id", 1001);
    # query.bindValue(":forename", "Bart");
    # query.bindValue(":surname", "Simpson");
    # query.exec();
    # print(query.lastError())

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())