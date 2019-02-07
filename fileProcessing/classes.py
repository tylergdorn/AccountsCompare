# Defined classes for our data records

class Record:
    def __init__(self, invoiceNo, date, agencyName, totalDue, line):
        self.invoiceNo = invoiceNo
        self.date = date
        self.agencyName = agencyName
        self.totalDue = totalDue
        self.line = line

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __eq__(self, other):
        return self.invoiceNo == other.invoiceNo and self.totalDue == other.totalDue