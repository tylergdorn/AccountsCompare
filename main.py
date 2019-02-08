import fileProcessing as fp
from fileProcessing import process
from fileProcessing import compare

alProList = process.loadAlProCSV('./data/ALProExportt.TXT')
QBList = process.loadQBFile('./data/2018 QBs Invoice Listing.xlsx')
print('done')
print(QBList[0])
compare.compare(alProList, QBList)

