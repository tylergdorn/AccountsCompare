"""Process is where we load all files into a standard format"""

import csv
from openpyxl import load_workbook
from typing import List

from fileProcessing import classes
from fileProcessing import errors

@errors.FileLoadDecorator
def loadAlProCSV(filePath: str) -> List[classes.Record]:
    """
    This loads an AL-Pro CSV file with '\t' as the delimiter. We may need to change this to accommodate better cases.
    This returns an array of Records
    """
    res = []
    with open(filePath, 'r', encoding="utf8", errors="replace") as csvfile:
        csvReader = csv.reader(csvfile, delimiter='\t')
        next(csvReader) # skip the header
        i = 1
        for row in csvReader:
            i += 1 # counting the line numbers the lazy way
            # pass it all into Record
            record = classes.Record(row[0], row[1], row[2], row[3] if row[3] else 0, i, True)
            res.append(record)
    csvfile.close()
    return res

@errors.FileLoadDecorator
def loadQBFile(filePath: str) -> List[classes.Record]:
    """
    This method loads a given file and returns an array of Records. A lot of this is hardcoded in so if the format of the QB file changes we will need to fix that. 
    We might want to think of a better way to do this.
    """
    wb = load_workbook(filename=filePath, read_only=True)
    # Load the worksheet
    ws = wb['Sheet1']
    # using a hashmap so we can consolidate the values down
    consolidate = {}
    # magic number 3 is because after 3 is where the important data starts
    ws.calculate_dimension(force=True)
    for index, item in enumerate(ws.rows):
        # iterate through all rows and load them into our array
        # minus two because of the annoying sum at the bottom
        if 2 <= index < (ws.max_row - 2):
            record = _loadRow(item, index)
            if record:
                record.invoiceNo = record.invoiceNo[:5]
                if record.invoiceNo in consolidate:
                    # if there is a collision we add the line number for usability and increment the totaldue amount
                    consolidate[record.invoiceNo].totalDue += record.totalDue
                    consolidate[record.invoiceNo].line.append(record.line)
                else:
                    consolidate[record.invoiceNo] = record
        # make a list out of the values so we can iterate
    wb.close()
    return list(consolidate.values())
    
def _loadRow(row, rowNo) -> classes.Record:
    """_loadRow takes a row from a openpyxl workbook and returns a Record corresponding to the row. the Row no is passed along just to build the Record"""
    # A bit weird here. the numbers correspond to the position in a row, ie H is 7
    # extra weird now that I added stuff. Apparently we only care about the accounts receiveable because that's how accounting works
    return classes.Record(row[7].value, row[5].value, row[9].value, row[21].value, rowNo, False) if "Accounts Receivable" in row[13].value else None
