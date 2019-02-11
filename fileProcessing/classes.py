# Defined classes for our data records

class Record: 
    def __init__(self, invoiceNo, date, agencyName, totalDue, line, alPro):
        self.invoiceNo = invoiceNo
        self.date = date
        self.agencyName = agencyName
        self.totalDue = int(float(totalDue) * 100)
        self.line = [] 
        self.line.append(line)
        self.alPro = alPro

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __eq__(self, other):
        return self.invoiceNo == other.invoiceNo and self.totalDue == other.totalDue

def intToStr(number):
    return f'{number // 100}.{number % 100}'

class MissingResult:
    def __init__(self, record):
        self.record = record
        self.recordType = 'Al-Pro' if self.record.alPro else 'Quickbooks'
        self.otherType = 'Al-Pro' if not self.record.alPro else 'Quickbooks'
        
    def __str__(self):
       return f'{self.recordType} invoice number {self.record.invoiceNo} - {self.record.agencyName} not found in {self.otherType}'

class MismatchResult:
    def __init__(self, record, other):
        self.record = record
        self.other = other
        self.recordType = 'Al-Pro' if self.record.alPro else 'Quickbooks'
        self.otherType = 'Al-Pro' if self.other.alPro else 'Quickbooks'

    def __str__(self):
        return f'{self.recordType} Invoice number {self.record.invoiceNo} - {self.record.agencyName} amount {intToStr(self.record.totalDue)} does not match {self.otherType} amount {intToStr(self.other.totalDue)}'
    