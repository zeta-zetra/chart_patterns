import pandas as pd 
import pytest
import os 



from chart_patterns.chart_patterns.head_and_shoulders import find_head_and_shoulders


def test_find_head_and_shoulders():
    """
    Test finding the head and shoulders pattern
    """
    
    ohlc = pd.read_csv("./data/eurusd-4h.csv")
    ohlc = ohlc.iloc[4100:4400,:].reset_index()
    ohlc = find_head_and_shoulders(ohlc)
    df = ohlc[ohlc["hs_idx"].str.len()>0]
    assert df.shape[0] == 1