import pandas as pd 
import pytest
import os

from chart_patterns.chart_patterns.pennant import find_pennant


def test_find_pennant():
    """
    Test finding the pennant patterns
    """
    
    ohlc = pd.read_csv("./data/eurusd-4h.csv")
    ohlc = ohlc.iloc[3400:3600,:].reset_index()
    ohlc = find_pennant(ohlc)
    df   = ohlc[ohlc["pennant_point"]>0]
    assert df.shape[0] == 4     