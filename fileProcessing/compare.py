"""compare is where our comparison code lives, and serves to compare the two lists of items"""

from typing import List, Union

import fileProcessing.classes as classes
import fileProcessing.errors as fperrors

@fperrors.ComparisonDecorator
def compare(alProList: List[classes.Record], QBList: List[classes.Record]) -> List[classes.Result]:
    """This takes a list of records corresponding to the Al-Pro items and QBList and returns a list of MissingResults and MismatchResults"""
    alproDictionary = {} 
    count = 0
    errors: List[classes.Result] = []

    # we load all the alpro errors into a dict
    for item in alProList:
        alproDictionary[item.invoiceNo] = item

    for item in QBList:
        # Then we look at each quickbook item and check if they're there
        if item.invoiceNo not in alproDictionary:
            # this is pass because we don't care about items in qb not in alpro
            pass
        # We check then if they're there if the amount due matches the expected amount (the alpro amount)
        elif alproDictionary[item.invoiceNo].totalDue != item.totalDue:
            errors.append(classes.MismatchResult(item, alproDictionary[item.invoiceNo]))
            # we delete if it doesn't match, because it has been dealt with
            del alproDictionary[item.invoiceNo]
        else:
            # we delete it if it matches
            del alproDictionary[item.invoiceNo]
            count += 1
    # after we look through all of them, we go through the remaining ones since those are not in the list of quickbook items
    for item in alproDictionary.values():
        errors.append(classes.MissingResult(item))
    # return errors sorted by invoice number
    return sorted(errors, key=lambda errorRes: errorRes.record.invoiceNo)