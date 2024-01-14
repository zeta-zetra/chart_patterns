"""
Date  : 2023-12-25
Author: Zetra Team

"""

import numpy as np
import pandas as pd 

from chart_patterns.chart_patterns.utils import check_ohlc_names
from typing import Union



def find_pivot_point(ohlc: pd.DataFrame, current_row: int, left_count:int = 3, right_count:int =3) -> int:
    """
    Check if the current row (i.e. point) is a pivot point
    
    :params ohlc is a dataframe with Open, High, Low, Close data
    :type :pd.DataFrame
    
    :params current_row is the index number of the row 
    :type :int
    
    :params left_count is the number of candles to the left to consider
    :type :int 
    
    :params right_count is the number of candles to right to consider 
    :type :int
    
    :return (int) 
    """
 
    # Check if ohlc dataframe meets certain conditions
    check_ohlc_names(ohlc)
    
    
    # Check if the length conditions are met
    if current_row - left_count < 0 or current_row + right_count >= len(ohlc):
        return 0
    
    pivot_low  = 1
    pivot_high = 1

    for idx in range(current_row - left_count, current_row + right_count + 1):
        if(ohlc.loc[current_row, "low"] > ohlc.loc[idx, "low"]):
            pivot_low = 0

        if(ohlc.loc[current_row, "high"] < ohlc.loc[idx, "high"]):
            pivot_high = 0

    if pivot_low and pivot_high:
        return 3

    elif pivot_low:
        return 1

    elif pivot_high:
        return 2
    else:
        return 0

def find_all_pivot_points(ohlc: pd.DataFrame, left_count:int = 3, right_count:int = 3, name_pivot: Union[None, str] = None ) -> pd.DataFrame:
    """
    Find the all the pivot points for the given OHLC dataframe

    :params ohlc is a dataframe with Open, High, Low, Close data
    :type :pd.DataFrame
    
    :params left_count is the number of candles to the left to consider
    :type :int 
    
    :params right_count is the number of candles to right to consider 
    :type :int 
    
    :return (pd.DataFrame)
    """


    if name_pivot != None:
        ohlc[name_pivot] = ohlc.apply(lambda row: find_pivot_point(ohlc, row.name, left_count, right_count), axis=1)
        ohlc[f"{name_pivot}_pos"] =  ohlc.apply(lambda row: find_pivot_point_position(row), axis=1)
    else:
        # Get the pivot points 
        ohlc["pivot"]     = ohlc.apply(lambda row: find_pivot_point(ohlc, row.name, left_count, right_count), axis=1)
        ohlc['pivot_pos'] = ohlc.apply(lambda row: find_pivot_point_position(row), axis=1)


    return ohlc 


def find_pivot_point_position(row: pd.Series) -> float:
    """
    Get the Pivot Point position and assign the Low or High value.  

    :params row to assign the pivot point position value if applicable. There must be a 'pivot' value
    :type :pd.Series 
    
    :return (float)
    """
   
   
    try:
        if row['pivot']==1:
            return row['low']-1e-3
        elif row['pivot']==2:
            return row['high']+1e-3
        else:
            return np.nan

    except Exception as e:
        print(f"Error: {e}")
        return np.nan
    
if __name__ == "__main__":
    import os
    # print(os.path.realpath('').split("\patterns")[0])
    data = pd.read_csv(os.path.join(os.path.realpath('').split("\patterns")[0],"data","eurusd-4h.csv"))
    
    # print(find_all_pivot_points(data))
    data = find_all_pivot_points(data)
    display_pivot_points(data)
    