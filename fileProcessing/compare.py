def compare(alProList, QBList):
    expDict = {} 
    count = 0
    for item in alProList:
        expDict[item.invoiceNo] = item
    for item in QBList:
        if item.invoiceNo not in expDict:
            pass
            # print(f'QB item {item.invoiceNo} not in Al-Pro List!')
        elif expDict[item.invoiceNo].totalDue != item.totalDue:
            # print(f'ALpro Amount {expDict[item.invoiceNo].invoiceNo} does not equal amount for qb item {item.invoiceNo}')
            del expDict[item.invoiceNo]
        else:
            count += 1
    print(count)
    # for item in expDict:
        # print(f'Unmatched Alpro item {expDict[item].invoiceNo}!')