import fileProcessing as fp
from fileProcessing import process
from fileProcessing import compare

alProList = process.loadAlProCSV('./data/ALProExport.TXT')
QBList = process.loadQBFile('./data/2018 QBs Invoice Listing.xlsx')

errors = compare.compare(alProList, QBList)
for item in errors:
    print(item)