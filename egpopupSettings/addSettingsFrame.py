from tkinter import *
from tkinter.ttk import Notebook

import subprocess
import os.path
import json

from eguanaModel import EguanaModel

from egpopupSettings.groupDescriptionCheckboxFrame import GroupDescriptionCheckboxFrame
from egpopupSettings.groupEditCheckboxFrame import GroupEditCheckboxFrame
from helpers import jsonHelper

GROUP_DEFAULT_STRING = "Enter your group name"
DUPLICATE_NAME_ERROR = "The group name you entered already exists. Please try again."

class AddSettingsFrame(Frame):

    def __init__(self, notebook, parent):
        Frame.__init__(self,notebook)
        
        self.parent = parent
        self.currentTypeValue = None
        self.currentMachineTypeValue = None
        self.currentFilterFunctionValue = None
        self.currentHeadFilterTypeValue = None
        self.currentJawFilterTypeValue = None

        self.setupFrame()

    def setupFrame(self):
        dropList = ['Machine', 'Head Filter','Jaw Filter','Module','Group']
        dropTitle = StringVar()
        dropTitle.set('Select Type')
        drop = OptionMenu(self, dropTitle, *dropList, command=self.selectTypeCallback)
        drop.grid(row=0, column=0, columnspan=4, sticky='ew')
        
        self.currentValue = None

        for row in range(0, 5):
            self.rowconfigure(row, weight=1)

        for col in range(0, 4):
            self.columnconfigure(col, weight=1)

    def selectTypeCallback(self, value):
        if value != self.currentValue:
            self.currentValue = value

            for i in range(1, self.grid_size()[1]):
                for element in self.grid_slaves(i, None):
                    element.grid_forget()

            if value == 'Machine':
                loadButton = Button(self, text='Load config file', relief=RAISED, command=lambda: self.machineLoadButtonPressed(loadButton))
                loadButton.grid(row=1, column=0, columnspan=4, sticky=E+W)

            elif value == 'Head Filter':
                loadButton = Button(self, text='Load config file', relief=RAISED, command=lambda:self.headFilterTypeLoadButtonPressed(loadButton))
                loadButton.grid(row=1, column=0, columnspan=4, sticky=E+W)

            elif value == 'Jaw Filter':
                loadButton = Button(self, text='Load config file', relief=RAISED, command=lambda:self.jawFilterTypeLoadButtonPressed(loadButton))
                loadButton.grid(row=1, column=0, columnspan=4, sticky=E+W)

            elif value == 'Module':
                loadButton = Button(self, text='Load config file', relief=RAISED, command=lambda:self.moduleLoadButtonPressed(loadButton))
                loadButton.grid(row=1, column=0, columnspan=4, sticky=E+W)
            else: #group
                self.setupAddGroup();

    def machineLoadButtonPressed(self, loadButton):
        filePath = filedialog.askopenfilename(filetypes=[('Python file','*.py')])
        
        if filePath != '':
            components = filePath.split('/')
            fileName = components[-1]

            if os.path.isfile(os.getcwd()+'/machineConfig/'+fileName) == False:
                # [isValid, errorString] = MachineConfigTest(filePath).runTests() //TODO
                isValid = 1

                if isValid:
                    loadButton.config(text=filePath)

                    groupDesctiptionNotebook = Notebook(self)
                    groupDesctiptionNotebook.grid(row=2, column=0, columnspan=4, sticky=E+W)
                    

                    tabNameList = jsonHelper.getAllGroups()
                    groupDescriptionFrameList = [];

                    for tabName in tabNameList:
                        groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, tabName)
                        groupDescriptionFrameList.append(groupDescriptionFrame)
                        groupDescriptionFrame.pack(fill=BOTH, expand=True)
                        groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabName)
                      

                    Button(self, text='Apply & Close', relief=RAISED, command=lambda: self.applyMachineButtonPressed(filePath, groupDescriptionFrameList)).grid(row=3,column=1,columnspan=1,sticky=S+E)
                
                else:
                    messagebox.showinfo("Error", errorString)

            else:
                messagebox.showinfo("Error", "File already exists in machineConfig directory: " + fileName)

    def headFilterTypeLoadButtonPressed(self, loadButton):
        filePath = filedialog.askopenfilename()
        if filePath:
            components = filePath.split('/')
            fileName = components[-1]

            if not os.path.isfile(os.getcwd()+'/filterTypesConfig/headFilters/'+fileName):
                # [isValid, errorString] = FilterTypesConfigTest(filePath).runTests()
                isValid = True
                
                if isValid:
                    loadButton.config(text=filePath)
                    self.filterTypeLoadButtonPressed(filePath,'Head')
                
                else:
                    messagebox.showinfo("Error","")
            else:
                messagebox.showinfo("Error", "File already exists in directory: " + fileName)

    def jawFilterTypeLoadButtonPressed(self, loadButton):
        filePath = filedialog.askopenfilename()
        if filePath:
            components = filePath.split('/')
            fileName = components[-1]

            if not os.path.isfile(os.getcwd()+'/filterTypesConfig/jawFilters/'+fileName):
                # [isValid, errorString] = FilterTypesConfigTest(filePath).runTests()
                isValid = True
                
                if isValid:
                    loadButton.config(text=filePath)
                    self.filterTypeLoadButtonPressed(filePath,'Jaw')
                
                else:
                    messagebox.showinfo("Error","")
            else:
                messagebox.showinfo("Error", "File already exists in directory: " + fileName)

    def filterTypeLoadButtonPressed(self, filePath,filterType):
        groupDesctiptionNotebook = Notebook(self)
        groupDesctiptionNotebook.grid(row=2, column=0, columnspan=4, sticky=E+W)

        tabNameList = jsonHelper.getAllGroups()
        groupDescriptionFrameList = [];

        for tabName in tabNameList:
            groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, tabName)
            groupDescriptionFrameList.append(groupDescriptionFrame)
            groupDescriptionFrame.pack(fill=BOTH, expand=True)
            groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabName)
          
        Button(self, text='Apply & Close',relief=RAISED,command=lambda:self.applyFilterTypeButtonPressed(filePath, groupDescriptionFrameList, filterType)).grid(row=3,column=1,columnspan=1,sticky=S+E)

    def moduleLoadButtonPressed(self,loadButton):
        filePath = filedialog.askopenfilename(filetypes=[('Python file','*.py')])
        
        if filePath:
            components = filePath.split('/')
            fileName = components[-1]

            if not os.path.isfile(os.getcwd()+'/moduleConfig/'+fileName):
                # [isValid, errorString] = MachineConfigTest(filePath).runTests() //TODO
                isValid = True

                if isValid:
                    loadButton.config(text=filePath)

                    groupDesctiptionNotebook = Notebook(self)
                    groupDesctiptionNotebook.grid(row=2, column=0, columnspan=4, sticky=E+W)
                    
                    tabNameList = jsonHelper.getAllGroups()
                    groupDescriptionFrameList = [];

                    for tabName in tabNameList:
                        groupDescriptionFrame = GroupDescriptionCheckboxFrame(groupDesctiptionNotebook, tabName)
                        groupDescriptionFrameList.append(groupDescriptionFrame)
                        groupDescriptionFrame.pack(fill=BOTH, expand=True)
                        groupDesctiptionNotebook.add(groupDescriptionFrame, text=tabName)
                      
                    Button(self,text='Apply & Close',relief=RAISED, command=lambda: self.applyModuleButtonPressed(filePath, groupDescriptionFrameList)).grid(row=3,column=1,columnspan=1,sticky=S+E)
                
                else:
                    messagebox.showinfo("Error", errorString)
            else:
                messagebox.showinfo("Error", "File already exists in moduleConfig directory: " + fileName)

    def setupAddGroup(self):
        
        groupNameEntry = Entry(self,justify=CENTER);
        groupNameEntry.insert(0, GROUP_DEFAULT_STRING)
        groupNameEntry.bind('<FocusIn>', lambda event:self.on_entry_click(event,groupNameEntry))
        groupNameEntry.bind('<FocusOut>', lambda event:self.on_focusout(event,groupNameEntry))
        groupNameEntry.config(fg = 'grey')
        groupNameEntry.grid(row=1,column=1,columnspan=2,sticky=E+W)
        groupCheckboxFrame = GroupEditCheckboxFrame(self,jsonHelper.getAllHeadFiltersFileNames(),jsonHelper.getAllJawFiltersFileNames(),jsonHelper.getAllModulesFileNames())
        groupCheckboxFrame.grid(row=2, column=0, columnspan=4, sticky=E+W+N+S)
        Button(self,text='Apply & Close',relief=RAISED,command=lambda:self.applyGroupButtonPressed(groupNameEntry.get(),groupCheckboxFrame)).grid(row=3,column=1,columnspan=1,sticky=S+E)

    def applyMachineButtonPressed(self, filePath, groupDescriptionFrameList):
        
        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addMachineToJSON(fileName,groupNameList)

        subprocess.call('cp \"'+filePath+'\" ./machineConfig/', shell=True)
        self.parent.destroy()

    def applyFilterTypeButtonPressed(self, filePath, groupDescriptionFrameList, filterType):
        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addFilterTypeToJSON(fileName,groupNameList,filterType)

        if filterType == 'Head':
            subprocess.call('cp \"'+filePath+'\" ./filterTypesConfig/headFilters/', shell=True)
        else:
            subprocess.call('cp \"'+filePath+'\" ./filterTypesConfig/jawFilters/', shell=True)

        self.parent.destroy()

    def applyModuleButtonPressed(self, filePath, groupDescriptionFrameList):
        components = filePath.split('/')
        fileName = components[-1]

        groupNameList = []

        for groupDescriptionFrame in groupDescriptionFrameList:
            if groupDescriptionFrame.isEnabled():
                groupNameList.append(groupDescriptionFrame.groupName)

        jsonHelper.addModuleToJSON(fileName,groupNameList)

        subprocess.call('cp \"'+filePath+'\" ./moduleConfig/', shell=True)
        self.parent.destroy()

    def applyGroupButtonPressed(self,groupName, groupCheckboxFrame):

        groupNameList = jsonHelper.getAllGroups()

        if groupName in groupNameList:
            messagebox.showinfo("Error", DUPLICATE_NAME_ERROR)
        else:
            headFilterFilenameList = groupCheckboxFrame.getEnabledHeadFilenames() 
            jawFilterFilenameList = groupCheckboxFrame.getEnabledJawFilenames() 
            moduleFilenameList = groupCheckboxFrame.getEnabledModuleFilenames() 
            jsonHelper.addGroupToJSON(groupName,headFilterFilenameList,jawFilterFilenameList,moduleFilenameList)
            self.parent.destroy()



    def on_entry_click(self,event,groupNameEntry):
        """function that gets called whenever entry is clicked"""
        if groupNameEntry.get() == GROUP_DEFAULT_STRING:
           groupNameEntry.delete(0, "end") # delete all the text in the entry
           groupNameEntry.insert(0, '') #Insert blank for user input
           groupNameEntry.config(fg = 'black')

    def on_focusout(self,event,groupNameEntry):
        if groupNameEntry.get() == '':
            groupNameEntry.insert(0, GROUP_DEFAULT_STRING)
            groupNameEntry.config(fg = 'grey')

