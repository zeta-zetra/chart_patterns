"""
Date  : 2024-01-09
Author: Zetra Team

"""

import numpy as np
import pandas as pd 


from typing import Tuple


def find_points(ohlc: pd.DataFrame, candle_idx: int, lookback: int) -> Tuple[np.array, np.array, np.array, int, int, int, int]:
    """
    Find points provides all the necessary arrays and data of interest

    
    :params ohlc is the OHLC dataframe that has the pivot points
    :type :pd.DataFrame
    
    :params candle_idx is the candlestick index of interest
    :type :int 
    
    :params lookback is the number of back candlesticks to use 
    :type :int 
    
    :return (Tuple[np.array, np.array, np.array, int, int, int, int])    
    """

    maxim = np.array([])
    minim = np.array([])
    xxmin = np.array([])
    xxmax = np.array([])
    minbcount     = 0 #minimas before head
    maxbcount     = 0 #maximas before head
    minacount     = 0 #minimas after head
    maxacount     = 0 #maximas after head
    half_lookback = int(lookback/2)
    
    idx = candle_idx - half_lookback
    for i in range(idx-half_lookback, idx + half_lookback):
        if ohlc.loc[i,"short_pivot"] == 1:
            minim = np.append(minim, ohlc.loc[i, "low"])
            xxmin = np.append(xxmin, i)        
            if i < idx:
                minbcount+=1
            elif i> idx:
                minacount+=1
        if ohlc.loc[i, "short_pivot"] == 2:
            maxim = np.append(maxim, ohlc.loc[i, "high"])
            xxmax = np.append(xxmax, i)
            if i < idx:
                maxbcount+=1
            elif i> idx:
                maxacount+=1
    
    return maxim, minim, xxmax, xxmin, maxacount, minacount, maxbcount, minbcount