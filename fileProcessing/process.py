"""Process is where we load all files into a standard format"""

import csv
from openpyxl import load_workbook
from typing import List, Union

from fileProcessing import classes
from fileProcessing import errors

class qbFormat:
    """Holder for the format of our quickbooks file"""
    def __init__(self, num: int, date: int, name: int, amount: int, account: int):
        self.num = num
        self.date = date
        self.name = name
        self.amount = amount
        self.account = account

def findQBHeader(indexRow: List) -> qbFormat:
    """ When given the first row in a quickbooks export, it gives us a qbFormat of where to find all the data in each row"""
    indexes = [None] * 5
    for index, item in enumerate(indexRow):
        # check for the headers we want
        # print(f'value: "{item.value}" type: {type(item.value)}')
        if item.value == "Num":
            indexes[0] = index
        elif item.value == "Date":
            indexes[1] = index
        elif item.value == "Name":
            indexes[2] = index
        elif item.value == "Amount":
            indexes[3] = index
        elif item.value == "Account":
            indexes[4] = index
    for item in indexes:
        # if any of them are still None we raise an error
        if not item:
            raise errors.FileLoadError("Failed to load quickbooks header")
    # sick hack here to make my life easier
    return qbFormat(*indexes)

@errors.FileLoadDecorator
def loadAlProCSV(filePath: str) -> List[classes.Record]:
    """
    This loads an AL-Pro CSV file with '\t' as the delimiter. We may need to change this to accommodate better cases.
    This returns an array of Records
    """
    res = []
    with open(filePath, 'r', encoding="utf8", errors="replace") as csvfile:
        csvReader = csv.DictReader(csvfile, delimiter='\t')
        i = 1
        for row in csvReader:
            i += 1 # counting the line numbers the lazy way
            # check if it's negative the lazy way
            if row["TotalDue"][0] != '-':
                # pass it all into Record if it's not negative
                record = classes.Record(row["InvoiceNo"], row["InvoiceDate"], row["AgencyName"], row["TotalDue"] if row["TotalDue"] else 0, i, True)
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
    # we find the rows we want
    header = findQBHeader(next(ws.rows))
    # print(ws.max_row)
    for index, item in enumerate(ws.rows):
        # iterate through all rows and load them into our array
        # minus two because of the annoying sum at the bottom
        if 1 <= index < (ws.max_row - 3):
            record = _loadRow(item, index, header)
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
    
def _loadRow(row: List, rowNo: int, head: qbFormat) -> Union[classes.Record, None]:
    """_loadRow takes a row from a openpyxl workbook and returns a Record corresponding to the row. the Row no is passed along just to build the Record"""
    """ Returns None if we don't care about the row in question"""
    # if this is accounts receivable we return none. else we use the header data to tell us where to get the info
    return classes.Record(row[head.num].value, row[head.date].value, row[head.name].value, row[head.amount].value, rowNo, False) if "Accounts Receivable" in row[head.account].value else None
