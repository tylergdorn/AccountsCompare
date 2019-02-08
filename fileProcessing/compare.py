import fileProcessing.classes as classes
def compare(alProList, QBList):
    expDict = {} 
    count = 0
    errors = []
    for item in alProList:
        expDict[item.invoiceNo] = item
    for item in QBList:
        if item.invoiceNo not in expDict:
            errors.append(classes.MissingResult(item))
        elif expDict[item.invoiceNo].totalDue != item.totalDue:
            errors.append(classes.MismatchResult(item, expDict[item.invoiceNo]))
            del expDict[item.invoiceNo]
        else:
            count += 1
            
    for item in expDict.values():
        errors.append(classes.MissingResult(item))
    return errors#.sort(key=lambda item: item.record.invoiceNo)