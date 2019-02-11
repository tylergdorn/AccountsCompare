# Defined classes for our data records

class Record: 
    """Record is the holder for a sequence of data corresponding to a line in the csv or xlsx documents"""
    def __init__(self, invoiceNo, date, agencyName, totalDue, line, alPro):
        self.invoiceNo = invoiceNo
        self.date = date
        self.agencyName = agencyName
        # float addition works bad, but the value we scrape is in the form 123.45
        self.totalDue = int(float(totalDue) * 100)
        self.line = [] 
        self.line.append(line)
        self.alPro = alPro

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __eq__(self, other):
        return self.invoiceNo == other.invoiceNo and self.totalDue == other.totalDue

def intToStr(number: int) -> str:
    """Helper function that takes an int representing a number of cents and returns a string representing a number of """
    return f'{number // 100}.{number % 100}'

class MissingResult:
    """The holder for an error where one record is not present in the other"""
    def __init__(self, record: Record):
        self.record = record
        self.recordType = 'Al-Pro' if self.record.alPro else 'Quickbooks'
        self.otherType = 'Al-Pro' if not self.record.alPro else 'Quickbooks'
        
    def __str__(self):
       return f'{self.recordType} invoice number {self.record.invoiceNo} - {self.record.agencyName} not found in {self.otherType}'

class MismatchResult:
    """The holder for the error where the totalDue of one is not the totalDue of the other"""
    def __init__(self, record: Record, other: Record):
        self.record = record
        self.other = other
        self.recordType = 'Al-Pro' if self.record.alPro else 'Quickbooks'
        self.otherType = 'Al-Pro' if self.other.alPro else 'Quickbooks'

    def __str__(self):
        return f'{self.recordType} Invoice number {self.record.invoiceNo} - {self.record.agencyName} amount {intToStr(self.record.totalDue)} does not match {self.otherType} amount {intToStr(self.other.totalDue)}'
    