import PySimpleGUI as sg      

text = sg.PopupGetFile('Please enter a file name')      
sg.Popup('Results', 'The value returned from PopupGetFile', text)      