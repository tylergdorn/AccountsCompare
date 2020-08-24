import pytest
from fileProcessing.classes import Record, MismatchResult, MissingResult
from fileProcessing import compare
from typing import List
import time

def test_trivial_compare_sucess() -> None:
    alpro: List[Record] = []
    quickbooks: List[Record] = []
    ap = Record('1', str(time.localtime()), 'test', '100', 1, True)
    qb = Record('1', str(time.localtime()), 'test', '100', 1, False)
    alpro.append(ap)
    quickbooks.append(qb)
    res = compare.compare(alpro, quickbooks)
    assert len(res) == 0

def test_trivial_compare_missing() -> None:
    alpro: List[Record] = []
    quickbooks: List[Record] = []
    ap = Record('1', str(time.localtime()), 'test', '100', 1, True)
    qb = Record('2', str(time.localtime()), 'test', '100', 1, False)
    alpro.append(ap)
    quickbooks.append(qb)
    res = compare.compare(alpro, quickbooks)
    assert len(res) == 1
    assert isinstance(res[0], MissingResult)

def test_trivial_compare_mismatch() -> None:
    alpro: List[Record] = []
    quickbooks: List[Record] = []
    ap = Record('1', str(time.localtime()), 'test', '100', 1, True)
    qb = Record('1', str(time.localtime()), 'test', '101', 1, False)
    alpro.append(ap)
    quickbooks.append(qb)
    res = compare.compare(alpro, quickbooks)
    assert len(res) == 1
    assert isinstance(res[0], MismatchResult)