import pandas as pd 
import pytest
import os 


from chart_patterns.chart_patterns.triangles import find_triangle_pattern



def test_find_ascending_triangle():
    """ Test finding the ascending triangle pattern """
    
    ohlc = pd.read_csv("./data/eurusd-4h.csv")
    ohlc = ohlc.iloc[7200:7400,:].reset_index()
    ohlc = find_triangle_pattern(ohlc, triangle_type = "ascending")
    df   = ohlc[ohlc["triangle_point"]>0]
    assert df.shape[0] == 1
    
def test_find_descending_triangle():
    """ Test finding the descending triangle pattern """
    
    ohlc = pd.read_csv("./data/eurusd-4h.csv")
    ohlc = ohlc.iloc[19100:19280,:].reset_index()
    ohlc = find_triangle_pattern(ohlc, triangle_type = "descending")
    df   = ohlc[ohlc["triangle_point"]>0]
    assert df.shape[0] == 6
    
    
def test_find_symmetrical_triangle():
    """ Test finding the symmetrical triangle pattern """
    ohlc = pd.read_csv("./data/eurusd-4h.csv")
    ohlc = ohlc.iloc[:160,:].reset_index()
    ohlc = find_triangle_pattern(ohlc, triangle_type = "symmetrical")
    df   = ohlc[ohlc["triangle_point"]>0]
    assert df.shape[0] == 3