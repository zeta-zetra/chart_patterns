import pandas as pd 
import pytest
import os 
import sys

from chart_patterns.chart_patterns.doubles import find_doubles_pattern



def test_find_doubles_bottom_pattern():
    """
    Test finding doubles bottom pattern 
    """
    ohlc = pd.read_csv("./data/eurusd-4h.csv") 

    ohlc = ohlc.iloc[:37,:]
    ohlc = ohlc.reset_index()    
    ohlc = find_doubles_pattern(ohlc, double="bottoms")
    df   = ohlc[ohlc["double_idx"].str.len()>0]
    assert df.shape[0] == 4    
    
    
def test_find_doubles_top_pattern():
    """
    Test finding doubles top pattern
    """
    
    ohlc = pd.read_csv("./data/eurusd-4h.csv")
    ohlc = ohlc.iloc[400:440,:].reset_index()
    
    ohlc = find_doubles_pattern(ohlc, double="tops")
    df   = ohlc[ohlc["double_idx"].str.len()>0]
    assert df.shape[0] == 2
    
    
