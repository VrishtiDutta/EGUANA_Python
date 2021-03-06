
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we use the pack manager
to position two buttons in the
bottom-right corner of the window. 

Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""
import os, os.path

from tkinter import *
from tkinter import filedialog, FLAT, PhotoImage, Menu, CENTER, S, NW,NE, SW,W,SE, E, Toplevel, Entry, messagebox, simpledialog
from tkinter import Tk, RIGHT, RAISED, ttk, Frame, Button, Label, Text, TOP,RIDGE, BOTH,BOTTOM, Y,X,W, N, LEFT, SUNKEN

from egdialogs import CoilNumDialog
from egmenu import EguanaMenu
from egpopup import FilterFunctionPopup
from egpopup import FilterTypePopup

from eguanaModel import EguanaModel

import math

from machineConfig.eguanaMachineConfig import EguanaMachineConfig

class EguanaInit(object):
    @staticmethod
    def get_eguana_root_dir_name():
        drive_name = os.path.splitdrive(sys.executable)[0]
        is_unix    = drive_name == ''
        is_windows = not is_unix

        if is_unix:
            eguana_root_dir = '/eguana'
        else:
            eguana_root_dir = drive_name+"\\\\eguana"
        return eguana_root_dir
    
    @staticmethod
    def eguana_root_dir_exists():
        eguana_dir_name = EguanaInit.get_eguana_root_dir_name()
        return os.path.exists(eguana_dir_name)

    # To do
    @staticmethod
    def create_eguana_root_dir():
        eguana_dir_name = EguanaInit.get_eguana_root_dir_name()
        #os.makedirs(eguana_dir_name)
        #os.chown(eguana_dir_name, int(os.getenv('SUDO_UID')), int(os.getenv('SUDO_GID')))
        print(os.getenv("SUDO_USER"))

class EguanaGUI(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()

        # if not EguanaInit.eguana_root_dir_exists():
        #     EguanaInit.create_eguana_root_dir()
        
    def initUI(self):
      
        self.parent.title("EGUANA")
        self.style = ttk.Style()        
        self.style.theme_use("alt")        
        
        self.photoName = "eguana.gif"
        self.frame = Frame(self, relief=FLAT, borderwidth=10,bg='#FADC46')

        self.frame.pack(fill=BOTH, expand=True)        
        self.pack(fill=BOTH, expand=True)
        
        self.setupMenuBar()
        self.setupTopBar()  
        
    def setupMenuBar(self):
        
        self.menubar = EguanaMenu(self.parent,self)
        self.parent.config(menu=self.menubar)

    def setupTopBar(self):
        
        self.supportedDevices = []        
        
        for fileName in [name for name in os.listdir('./machineConfig') if os.path.isfile('./machineConfig/' + name) and not name == 'eguanaMachineConfig.py' and  name.endswith('.py')]:
        # try:{
            components = fileName.split('.')
            fileName = components[0]
            className = fileName[0].upper() + fileName[1:]
            try:
                module = __import__("machineConfig."+fileName,fromlist=["machineConfig."])                        
                classVar = getattr(module,className)
            except:
                continue
            self.supportedDevices.append(classVar())
            # except:
            #     pass

        self.selectMachineFrame = Frame(self.frame,relief=FLAT,bg='#FADC46')
        self.selectMachineFrame.pack(fill=BOTH,expand=True)
        self.setupSelectMachineButtons()
        
    def setupSelectMachineButtons(self):

        numDevices = len(self.supportedDevices)
        numColumns = 3
        numRows = math.ceil((numDevices+1)/3)
        
        self.photo = PhotoImage(file="eguana.gif")
        self.photo = self.photo.subsample(2);
        self.photo_label = Label(self.selectMachineFrame,image=self.photo,borderwidth=0,highlightthickness=0)
        self.photo_label.configure(bg='#FADC46')
        self.photo_label.grid(row=int(numRows/2),column=1, sticky=N+S+E+W,padx=2,pady =2)
        self.photo_label.image = self.photo        
        
        index = 0
        for i in range(numRows):
            for j in range(numColumns):
                
                if not(j == 1 and i == int(numRows/2)) and (index < numDevices):
                    device = self.supportedDevices[index]
                    b = Button(self.selectMachineFrame,text=device.name,relief=RAISED, command=lambda device=device :self.machineButtonPressed(device))
                    b.grid(row=i,column=j, sticky=N+S+E+W,padx=2,pady =2)
                    index += 1

            
        for i in range(numRows):
            self.selectMachineFrame.rowconfigure(i,weight=1)
         
        for i in range(numColumns):
            self.selectMachineFrame.columnconfigure(i,weight=1)
            

    def machineButtonPressed(self,inputDevice):

        dirStr = filedialog.askdirectory()
        
        if len(dirStr) and inputDevice.isDirectoryValid(dirStr):

            inputDevice.setDirPath(dirStr)
            EguanaModel().machine = inputDevice

            self.selectMachineFrame.destroy()

            self.menubar.inputSelected()

            self.photo_label.destroy()

            dirStr = 'Input Path : '+dirStr


            
            self.selectPlotFrame = Frame(self.frame, relief=FLAT,bg='#FADC46')
            self.selectPlotFrame.pack(fill=BOTH,expand=True)
            self.selectPlotFrame.rowconfigure(0,weight=1)
            self.selectPlotFrame.rowconfigure(1,weight=2)
            self.selectPlotFrame.columnconfigure(0,weight=1)

            self.infoFrame = Frame(self.selectPlotFrame, relief=FLAT, bg='#FADC46')
            self.infoFrame.grid(row=0,column=0, sticky=N+S+E+W,padx=2,pady =2)
               
            
            self.machineNameLabel = Label(self.infoFrame, text=inputDevice.name,relief=FLAT)
            self.machineNameLabel.grid(row=0,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)

            self.directoryLabel = Label(self.infoFrame, text="No project currently selected",relief=FLAT)
            self.directoryLabel.grid(row=1,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            self.directoryLabel.config(text=dirStr)
            
        
            self.outputDirButton = Button(self.infoFrame,text="No output directory selected. Click to select an output directory ",relief=RAISED,fg='red',command=self.askOutputDirectory)
            self.outputDirButton.grid(row=2,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            
            
            self.filterButton = Button(self.infoFrame,text="No filter selected. Click to select a filter",relief=RAISED,fg='red',command=self.selectFilter)
            self.filterButton.grid(row=3,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
           
           
            self.trialLabel = Label(self.infoFrame,text="Trial Number",relief=FLAT,justify=RIGHT,anchor=E)
            self.trialLabel.grid(row=4,column=0, sticky=N+S+E+W,padx=2,pady =2)


            vcmd = (self.master.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            self.trialEntry = Entry(self.infoFrame,validate = 'key', validatecommand = vcmd)
            self.trialEntry.grid(row=4,column=1, sticky=N+S+E+W,padx=2,pady =2)

            self.infoFrame.columnconfigure(0, weight=1)
            self.infoFrame.columnconfigure(1, weight=1)
            self.infoFrame.rowconfigure(0, weight=1)
            self.infoFrame.rowconfigure(1, weight=10)
            self.infoFrame.rowconfigure(2, weight=10)
            self.infoFrame.rowconfigure(3, weight=10)
            self.infoFrame.rowconfigure(4, weight=10)

            self.showPlotTools()

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
                           
        if len(value_if_allowed)==0 : 
            return True
        
        if text in '0123456789.-+ ':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
            
    def askOutputDirectory(self):
        dirStr = filedialog.askdirectory()
        if len(dirStr):
            dirStr = 'Output Path : '+dirStr
            self.outputDirButton.config(text=dirStr)

            

    def showPlotTools(self):        
        
        
        f2= Frame(self.selectPlotFrame, relief=FLAT,bg='#FADC46')
        f2.grid(row=1,column=0,sticky=N+S+E+W,padx=10,pady =10)
        
        b1 = Button(f2,text='3D K',relief=RAISED,command= lambda:self.plotButtonPressed(1))
        b1.grid(row=0, column=0,sticky=N+S+E+W,padx=5,pady =5)

        b2 = Button(f2,text='3D Dist',relief=RAISED,command=lambda:self.plotButtonPressed(2))
        b2.grid(row=0, column=1,sticky=N+S+E+W,padx=5,pady =5)
        
        b3 = Button(f2,text='3D DP',relief=RAISED,command=lambda:self.plotButtonPressed(3))
        b3.grid(row=0, column=2,sticky=N+S+E+W,padx=5,pady =5)
        
        b4 = Button(f2,text='2D K',relief=RAISED,command=lambda:self.plotButtonPressed(4))
        b4.grid(row=1, column=0,sticky=N+S+E+W,padx=5,pady =5)

        b5 = Button(f2,text='2D Dist',relief=RAISED,command=lambda:self.plotButtonPressed(5))
        b5.grid(row=1, column=1,sticky=N+S+E+W,padx=5,pady =5)

        b6 = Button(f2,text='2D DP',relief=RAISED,command=lambda:self.plotButtonPressed(6))
        b6.grid(row=1, column=2,sticky=N+S+E+W,padx=5,pady =5)
        
        
    
        b1.config(state=EguanaModel().machine.plot3DKButtonState)
        b2.config(state=EguanaModel().machine.plot3DDstButtonState)
        b3.config(state=EguanaModel().machine.plot3DDpButtonState)
        b4.config(state=EguanaModel().machine.plot2DKButtonState)
        b5.config(state=EguanaModel().machine.plot2DDstButtonState)
        b6.config(state=EguanaModel().machine.plot2DDpButtonState)

        f2.columnconfigure(0, weight=1)
        f2.columnconfigure(1, weight=1)
        f2.columnconfigure(2, weight=1)

        f2.rowconfigure(0, weight=1)
        f2.rowconfigure(1, weight=1)
       
    def plotButtonPressed(self,number):
        trialNum = self.trialEntry.get()
        
        try:
            trialNum = int(trialNum)
            
            print(EguanaModel().machine.ifTrialExists(trialNum))
            if EguanaModel().machine.ifTrialExists(trialNum):
                self.plotFigure(number)
                return True             
            else:
                messagebox.showerror(
                    "Trial Number Error",
                    "The trial doesn't exist"
                    )     
                return False
        except ValueError:
            messagebox.showerror(
                "Trial Number Error",
                "Error with the trial number"
            )  
            return False
            
    def plotFigure(self,number):
        m =  CoilNumDialog(self.frame)
        if m.isSet():
            print(m.getValues())
            EguanaModel().machine.getDataForTrialNumber(number)
        
    def selectFilter(self):        
        ffPopup = FilterFunctionPopup(self)
        if ffPopup.selectedFilter is not None:
            EguanaModel().filterFunction = ffPopup.selectedFilter
            ftPopup = FilterTypePopup(self,ffPopup.selectedFilter)
            if (ftPopup.selectedHeadFilterType is not None) and (ftPopup.selectedHeadFilterType is not None):
                self.menubar.setSelectedFilters(ffPopup.selectedFilter,ftPopup.selectedHeadFilterType,ftPopup.selectedJawFilterType)
                EguanaModel().filterTypeHead = ftPopup.selectedHeadFilterType
                EguanaModel().filterTypeJaw = ftPopup.selectedJawFilterType
                EguanaModel().filterFunction = ffPopup.selectedFilter
                buttonText = '{} - Jaw Filter : {} - Head Filter {}'.format(ffPopup.selectedFilter.name,ftPopup.selectedJawFilterType.name, ftPopup.selectedHeadFilterType.name)
                self.filterButton.config(text=buttonText)


    def updateSelectedFilters(self,ffName,ftHeadName,ftJawName): 
        buttonText = '{} - Jaw Filter : {} - Head Filter {}'.format(ffName,ftHeadName,ftJawName)
        self.filterButton.config(text=buttonText)

    def changeImage(self):
        self.photo = PhotoImage(file=self.photoName)
        self.photo = self.photo.subsample(2);
        self.photo_label.image = self.photo  
        self.photo_label.config(image=self.photo)
        
        
        
    def cursorPosition(self,event):       
        if event.widget ==  self.openButton3D:
            if self.photoName == "eguana2.gif":
                self.photoName = "eguana.gif"
                self.changeImage()
                
        elif event.widget ==  self.openButton2D:
            if self.photoName == "eguana.gif":
                self.photoName = "eguana2.gif"
                self.changeImage()
                
def main():
    
    global app
    global root
    root = Tk()

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    
    root.geometry('%dx%d+%d+%d' % (sw, sh, 0, 0))
    
    app = EguanaGUI(root)

    root.mainloop()

if __name__ == '__main__':
    main()  