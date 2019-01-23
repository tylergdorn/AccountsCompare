import fileProcessing as fp
from fileProcessing import process

alProList = process.loadAlProCSV('./data/ALProExport.TXT')

process.loadQBFile('./data/2018 QBs Invoice Listing.xlsx')