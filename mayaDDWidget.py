# coding:utf-8
import sys, os
import copy
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from PySide2 import QtCore, QtGui
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import *
    from PySide import QtCore, QtGui
    from shiboken import wrapInstance

from functools import partial
from collections import OrderedDict
import math
import re,json,glob,string

import maya.cmds as cmds

class MayaDDWidget(QWidget):

    dropped = Signal()

    def __init__(self, parent=None):
        super(MayaDDWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.dropObj = None

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()

        if mimeData.hasText() and mimeData.hasFormat('application/x-maya-data'):
            event.accept()

        elif mimeData.hasFormat('application/x-maya-data'):
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        nodes = []
        if event.mimeData().hasFormat('application/x-maya-data'):
            nodes = cmds.ls(sl=True)
        elif mimeData.hasText():
            nodes = mimeData.text().split('\n')

        self.dropObj = nodes
        self.dropped.emit()
