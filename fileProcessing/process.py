import csv
from openpyxl import load_workbook

from fileProcessing import classes

def loadAlProCSV(filePath):
    """
    This loads an AL-Pro CSV file with ',' as the delimiter. We may need to change this to accomodate better cases.
    This returns an array of AlProRecords
    """
    res = []
    with open(filePath, 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        i = 1
        for row in csvReader:
            i += 1
            record = classes.AlProRecord(row[0], row[1], row[2], row[3], i)
            res.append(record)
    return res

def loadQBFile(filePath):
    """
    This method loads a given file and returns an array of QBRecords. A lot of this is hardcoded in so if the format of the QB file changes we will need to fix that. 
    We might want to think of a better way to do this.
    """
    wb = load_workbook(filename=filePath, read_only=True)
    # Load the worksheet
    ws = wb['Sheet1']
    print(_getLastRow(ws))
    
def _loadRow(worksheet, rowNo):
    row = str(rowNo)
    return classes.QBRecord(worksheet['H' + row], worksheet['F' + row], worksheet['J' + row], worksheet['V' + row], rowNo)

def _getLastRow(worksheet):
    row = 3
    isValue = True
    while isValue:
        # print(worksheet[f'D{row}'].value == 'Invoice')
        isValue = (worksheet[f'D{row}'].value == 'Invoice')
        row += 1
    return row