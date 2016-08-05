from tkinter import  DISABLED, NORMAL
import os, os.path


class FilterConfig():

    def __init__(self):
        self.buttonName = ""
        self.setupPlotAndFilterStates()
        self.dirPath = ""
        self.allowedFilterList =  []


    def setupPlotAndFilterStates(self):
        self.plot3DKButtonState = 'normal'
        self.plot3DDstButtonState = 'normal'
        self.plot3DDpButtonState = 'normal'
        self.plot2DKButtonState = 'normal'
        self.plot2DDstButtonState = 'normal'
        self.plot2DDpButtonState = 'normal'
        self.speech3DFilterButtonState = NORMAL
        self.swallow3DFilterButtonState = NORMAL
        self.speech2DFilterButtonState = NORMAL
        self.swallow2DFilterButtonState = NORMAL
                
    def whatsMyName(self):
        print("EguanaConfig")
        
    def readHeadFile(self,filename):
        return 1

    def isDirectoryValid(self, path):
        return

    def ifTrialExists(self, trialNum):
        return

    def setDirPath(self,path):
        self.dirPath = path   

    def getAllowedFilters(self):
        return         