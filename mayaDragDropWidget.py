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

import maya.OpenMayaUI as mui
import maya.cmds as cmds
import maya.mel as mel
import math
import re,json,glob,string
from collections import OrderedDict

from types import MethodType

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
    if mimeData.hasText():
        nodes = mimeData.text().split('\n')

    elif event.mimeData().hasFormat('application/x-maya-data'):
        nodes = cmds.ls(sl=True)

        if not nodes:
            QtGui.QMessageBox.information(None, 'Error', 'Node is not selected', QtGui.QMessageBox.Yes)

            event.ignore()
            return

    if (hasattr(self, "model")):
        model = self.model()
        if (hasattr(model, "setItem")):
            for node in nodes:
                item = QtGui.QStandardItem(node)
                item.setFlags(item.flags() and QtCore.Qt.ItemIsDragEnabled)
                model.setItem(model.rowCount(), 0, item)
            event.accept()
        elif (hasattr(self, "addItem")):
            for node in nodes:
                self.addItem(node)

    elif (hasattr(self, "text")):
        r = ".".join(nodes)
        self.setText(r)

    elif (hasattr(self, "addItem")):
        for node in nodes:
            self.addItem(node)


def mayaDragDropWidget(custom_cls):
    cls_str = "PySide.QtGui." + custom_cls
    component_path = str(cls_str).split('.')
    package_path   = component_path[:-1]
    package_name   = ".".join(package_path)
    class_name     = component_path[-1]
    __import__(str(package_name))
    cls = getattr(sys.modules[package_name],class_name)
    cls_inst = cls()
    cls_inst.dragEnterEvent = MethodType(dragEnterEvent, cls_inst, cls)
    cls_inst.dropEvent = MethodType(dropEvent, cls_inst, cls)

    cls_inst.setDragEnabled(True)
    cls_inst.setAcceptDrops(True)
    try:
        cls_inst.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
    except:
        pass

    return cls_inst
