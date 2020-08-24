import pytest
import unittest
from fileProcessing import process
import csv
import tempfile
import os
from typing import IO

def test_alpro() -> None:
    temp: IO[str] = tempfile.NamedTemporaryFile(mode='w+', delete=False)

    alPro_record = {
        'InvoiceNo': 19,
        'InvoiceDate': '7/7/2020',
        'AgencyName': 'DOO',
        'TotalDue': '1936.5'
    }
    writer = csv.DictWriter(temp, alPro_record.keys(), dialect=csv.excel_tab)
    writer.writerow(alPro_record)

    records = process.loadAlProCSV(temp.name)
    assert len(records) == 1
    assert records[0].agencyName == 'DOO'
    temp.close()
    os.unlink(temp.name)
