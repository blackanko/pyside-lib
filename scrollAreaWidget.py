# coding:utf-8
import sys, os
import copy
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from PySide import QtCore, QtGui


class ScrollAreaWidget(QWidget):

    def __init__(self, contents=None, parent=None):
        super(ScrollAreaWidget, self).__init__(parent)

        self.container = QVBoxLayout(self)
        self.setLayout(self.container)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.layout().addWidget(self.scrollArea)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(QMargins())

        self.scrollContentsWidget = contents

        self.initScrollContents()


    def initScrollContents(self):
        if not self.scrollContentsWidget:
            self.scrollContentsWidget = QWidget(self)

        self.scrollArea.setWidget(self.scrollContentsWidget)

    def setContents(self, contents):
        if not contents:
            return
        self.scrollContentsWidget = contents
        self.initScrollContents()
