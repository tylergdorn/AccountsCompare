# Defined classes for our data records

class AlProRecord:
    def __init__(self, invoiceNo, date, agencyName, totalDue, line):
        self.invoiceNo = invoiceNo
        self.date = date
        self.agencyName = agencyName
        self.totalDue = totalDue
        self.line = line

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class QBRecord:
    def __init__(self, invoiceNo, date, agencyName, totalDue, line):
        self.invoiceNo = invoiceNo
        self.date = date
        self.agencyName = agencyName
        self.totalDue = totalDue
        self.line = line

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)