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

path = "" # file full path
fileName = "template.ui"

if not path in sys.path :
    sys.path[0:0] = [ path ]
from mayaDragDropWidget import *

# Maya Widnow
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    mayaMainWindowPtr = mui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QMainWindow)
    return mayaMainWindow

class gui(QtGui.QMainWindow):

    def __init__(self, parent=getMayaWindow()):
        window = "test"
        if cmds.dockControl( "%s_dock"%window,ex=True) :
            cmds.deleteUI("%s_dock"%window,control=True)

        if cmds.window( "%sWindow"%window, query = True, exists = True ):
            cmds.deleteUI( "%sWindow"%window )

        super(gui, self).__init__(parent)
        # load ui file
        self.basePath =  path
        loader = QUiLoader()
        uiFilePath = os.path.join(self.basePath, fileName)
        self.UI = loader.load(uiFilePath)
        self.setObjectName("%sWindow"%window)
        self.setWindowTitle("test")

        # test dynamics widget

        self.DDList = mayaDragDropWidget("QListView")
        model = QtGui.QStandardItemModel()
        self.DDList.setModel(model);

        self.LT = mayaDragDropWidget("QLineEdit")
        self.LW = mayaDragDropWidget("QListWidget")

        self.container = QGridLayout(self.UI.centralwidget)
        self.UI.centralwidget.setLayout(self.container)
        self.container.addWidget(self.DDList)
        self.container.addWidget(self.LT)
        self.container.addWidget(self.LW)
        self.LW.addItem("aaa")



        # central widget setting
        self.setCentralWidget(self.UI)
        self.show()
        cmds.window( "%sWindow"%window,e=True, tlb=1, mb=1)
        allowedAreas = ['right', 'left']

        #cmds.dockControl( "%s_dock"%window,l=window,area='right', vis=True,w=400,content="%sWindow"%window, allowedArea=allowedAreas )
        self.setAttribute(Qt.WA_DeleteOnClose)




gui().show()
