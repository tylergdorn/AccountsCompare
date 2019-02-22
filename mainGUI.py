import PySimpleGUI as sg      
import logging
import fileProcessing as fp
from fileProcessing import process
from fileProcessing import compare
from fileProcessing import errors as err
import os

def processInput(alProFile, QBFile):
    """This takes the file names and interacts with fileProcessing and returns a list of all the errors recorded"""
    # catch all exceptions so we can get the right pop up
    try:
        alProList = process.loadAlProCSV(alProFile)
        QBList = process.loadQBFile(QBFile)
    except err.FileLoadError:
        sg.PopupError("Couldn't load files. You may have exported them wrong")
        exit(-1)
    try:
        # get all the errors that come up and print them all
        errors = compare.compare(alProList, QBList)
        results = []
        for item in errors:
            results.append(str(item))
        return '\n'.join(results)
    except err.ComparisonError:
        sg.PopupError("Couldn't compare files.")
        exit(-1)

def mainGui():
    """The main GUI code. This is essentially the new main as a gui"""
    # layout for the file selection window
    fileSelectionLayout = [
            [sg.Text('Al-Pro Export', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText(''), sg.FileBrowse()],
            [sg.Text('Quickbooks Export', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText(''), sg.FileBrowse()],
            [sg.Submit()]
    ]

    fileSelectionWindow = sg.Window('Accounts Compare').Layout(fileSelectionLayout)

    event, values = fileSelectionWindow.Read()
    fileSelectionWindow.Close()
    # if the event isn't none and values were supplied (the success case)
    if event and values[0] and values[1]:
        # process the input and get our text back
        result = processInput(values[0], values[1])
        # layout of the results
        resultLayout = [
            [sg.Multiline(default_text=result, size=(130, 30), disabled=True)],
            [sg.Text('Choose a folder to save process.log to', size=(30, 1), auto_size_text=False, justification='right'),
                sg.InputText(), sg.FolderBrowse()],
            [sg.Save(tooltip='Click to submit this window'), sg.Cancel()]
        ]

        # run the window
        resultWindow = sg.Window('Results').Layout(resultLayout)
        event, values = resultWindow.Read()

        # There's a save button. it allows us to choose where to save file file. If the values[1] is set that means the user has picked a location to save the file at.
        if event == 'Save':
            if values[1]:
                with open(os.path.join(values[1], 'comparison.log'), 'w') as file:
                    file.write(result)
            else:
                with open('comparison.log', 'w') as file:
                    file.write(result)
        resultWindow.Close()
# call our program
logging.basicConfig(level=logging.ERROR, filename="error.log")
mainGui()

