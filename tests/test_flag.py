import pandas as pd 
import pytest
import os

from chart_patterns.chart_patterns.flag import find_flag_pattern


def test_find_flag_pattern():
    """
    Test finding the flag pattern
    """
    ohlc = pd.read_csv("./data/eurusd-4h.csv")
    ohlc = ohlc.iloc[900:1200,:].reset_index()
    ohlc = find_flag_pattern(ohlc)
    df   = ohlc[ohlc["flag_point"]>0]
    assert df.shape[0] == 4 



    

