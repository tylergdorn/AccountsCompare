from typing import List

import fileProcessing.classes as classes
import fileProcessing.errors as errors

@errors.ComparisonDecorator
def compare(alProList: List[classes.Record], QBList: List[classes.Record]):
    """This takes a list of records corresponding to the Al-Pro items and QBList and returns a list of MissingResults and MismatchResults"""
    expDict = {} 
    count = 0
    errors = []
    # we load all the alpro errors into a dict
    for item in alProList:
        expDict[item.invoiceNo] = item
    for item in QBList:
        # Then we look at each quickbook item and check if they're there
        if item.invoiceNo not in expDict:
            errors.append(classes.MissingResult(item))
        # We check then if they're there if the amount due matches the expected amount (the alpro amount)
        elif expDict[item.invoiceNo].totalDue != item.totalDue:
            errors.append(classes.MismatchResult(item, expDict[item.invoiceNo]))
            # we delete if it doesn't match, because it has been dealt with
            del expDict[item.invoiceNo]
        else:
            # we delete it if it matches
            del expDict[item.invoiceNo]
            count += 1
    # after we look through all of them, we go through the remaining ones since those are not in the list of quickbook items
    for item in expDict.values():
        errors.append(classes.MissingResult(item))
    # return errors sorted by invoice number
    return sorted(errors, key=lambda error: error.record.invoiceNo)