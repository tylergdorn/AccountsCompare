# AccountsCompare

AccountsCompare compares an Al-Pro export file that is tab separated with the following format:

`InvoiceNo, InvoiceDate, AgencyName, TotalDue`

this includes a header

This is compared to a Quickbooks export file. The export file has a complicated format and is likely subject to change.
For an idea of the format you can look at fileProcessing/process.py

This returns a list of errors of records that don't match, records that don't exist in the other.

## Dependencies

1. PyInstaller
1. Openpyxl
1. SimplePyGUI
1. Tkinter