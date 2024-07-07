import pandas as pd 
import pytest
import os 


from chart_patterns.chart_patterns.inverse_head_and_shoulders import find_inverse_head_and_shoulders


def test_find_inverse_head_and_shoulders():
    """
    Test finding the inverse head and shoulders
    """
    
    ohlc = pd.read_csv("./data/eurusd-4h.csv")
    ohlc = ohlc.iloc[4700:5000,:].reset_index()
    ohlc = find_inverse_head_and_shoulders(ohlc)
    df = ohlc[ohlc["ihs_idx"].str.len()>0]
    assert df.shape[0] == 1