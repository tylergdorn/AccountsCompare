import csv
from openpyxl import load_workbook

from fileProcessing import classes

def loadAlProCSV(filePath):
    """
    This loads an AL-Pro CSV file with ',' as the delimiter. We may need to change this to accomodate better cases.
    This returns an array of Records
    """
    res = []
    with open(filePath, 'r', encoding="utf8", errors="replace") as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        i = 1
        for row in csvReader:
            i += 1
            record = classes.Record(row[0], row[1], row[2], row[3], i)
            res.append(record)
    return res

def loadQBFile(filePath):
    """
    This method loads a given file and returns an array of Records. A lot of this is hardcoded in so if the format of the QB file changes we will need to fix that. 
    We might want to think of a better way to do this.
    """
    wb = load_workbook(filename=filePath, read_only=True)
    # Load the worksheet
    ws = wb['Sheet1']
    rows = []
    # magic number 3 is because after 3 is where the important data starts
    ws.calculate_dimension(force=True)
    for index, item in enumerate(ws.rows):
        # iterate through all rows and load them into our array
        if 3 <= index <= ws.max_row:
            rows.append(_loadRow(item, index))
    return rows
    
def _loadRow(row, rowNo):
    # A bit weird here. the numbers correspond to the position in a row, ie H is 7
    return classes.Record(row[7].value, row[5].value, row[9].value, row[21].value, rowNo)
